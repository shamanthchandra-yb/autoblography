import os
import re
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from llama_index.readers.web import SimpleWebPageReader


# --- Configuration ---
# Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your PyCharm Run Config
from ai_hackathon_2025.prompt_constant import GDOC_GENERATE_KEY_HIGH_LEVEL_IDEA

PROJECT_ID = "hackathon-2025-463220"
LOCATION = "us-central1"
os.environ["GCLOUD_PROJECT"] = PROJECT_ID


def read_google_doc_multimodal(document_id: str) -> dict:
    """
    Reads a Google Doc, extracts all text (including hyperlink URLs),
    downloads all images, and reads all comments.
    Returns a dictionary with text, image paths, and comments.
    """
    print(f"📄 Reading Google Doc multimodally (ID: {document_id})...")

    # Scopes for both Docs and Drive APIs
    SCOPES = [
        'https://www.googleapis.com/auth/documents.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]

    # Authenticate using the environment variable
    creds, _ = google.auth.default(scopes=SCOPES)

    # Build both the Docs and Drive service clients
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # --- 1. Get the document structure from the Docs API ---
    try:
        document = docs_service.documents().get(documentId=document_id).execute()
    except HttpError as e:
        if e.resp.status == 403:
            print(f"   -> ❌ ERROR: Permission denied for Google Doc ID '{document_id}'. Ensure it's shared with the service account.")
            return None
        else:
            raise e

    doc_content = document.get('body').get('content')

    extracted_text = ""
    image_paths = []
    image_counter = 1

    # --- 2. Parse the document content for text, links, and images ---
    print("📝 Parsing document text, links, and images...")
    for element in doc_content:
        if 'paragraph' in element:
            para_elements = element.get('paragraph').get('elements')
            for el in para_elements:
                # Standard Text Run
                text_run = el.get('textRun')
                if text_run:
                    extracted_text += text_run.get('content')
                    text_style = text_run.get('textStyle', {})
                    link = text_style.get('link')
                    if link and 'url' in link:
                        extracted_text += f" ({link.get('url')}) "

                # Rich Link (like Google Doc previews)
                rich_link = el.get('richLink')
                if rich_link:
                    rich_link_props = rich_link.get('richLinkProperties')
                    if rich_link_props and 'uri' in rich_link_props:
                        url = rich_link_props.get('uri')
                        extracted_text += f" ({url}) "
                        print(f"   -> Found rich link: {url}")

                # Embedded Objects (Images, Smart Chips)
                inline_obj_element = el.get('inlineObjectElement')
                if inline_obj_element:
                    inline_obj_id = inline_obj_element.get('inlineObjectId')
                    if inline_obj_id:
                        inline_object = document.get('inlineObjects').get(inline_obj_id)
                        embedded_object = inline_object.get('inlineObjectProperties').get('embeddedObject')

                        if 'imageProperties' in embedded_object:
                            image_properties = embedded_object.get('imageProperties')
                            content_uri = image_properties.get('contentUri')

                            if content_uri:
                                print(f"🖼️  Found image. Attempting to download...")

                                try:
                                    resp, content = drive_service._http.request(content_uri)

                                    if resp.status == 200:
                                        image_filename = f"doc_image_{image_counter}.png"
                                        with open(image_filename, 'wb') as f:
                                            f.write(content)
                                        image_paths.append(image_filename)
                                        image_counter += 1
                                        print(f"   -> Saved as {image_filename}")
                                    else:
                                        print(f"   -> Failed to download image. Status: {resp.status}")

                                except HttpError as e:
                                    if e.resp.status == 403:
                                        print(f"   -> ⚠️ Skipping image download due to permissions issue (403 Forbidden).")
                                    else:
                                        print(f"   -> ❌ Skipping image download due to an HTTP error: {e}")
                                except Exception as e:
                                    print(f"   -> ❌ An unexpected error occurred during image download: {e}")

                        elif 'smartChip' in embedded_object:
                            smart_chip = embedded_object.get('smartChip')
                            link = smart_chip.get('link')
                            if link and 'url' in link:
                                url = link.get('url')
                                extracted_text += f" ({url}) "
                                print(f"   -> Found smart chip link: {url}")

                        else:
                            print(f"⚠️  Skipping non-image, non-smart-chip embedded object (e.g., Google Drawing).")

    # --- 3. Fetch comments using the Drive API ---
    print("💬 Fetching comments from the document...")
    extracted_comments = []
    try:
        comments = drive_service.comments().list(
            fileId=document_id,
            fields="comments(author/displayName, content)"
        ).execute()

        for comment in comments.get('comments', []):
            author = comment.get('author', {}).get('displayName', 'Unknown Author')
            content = comment.get('content', '').replace('\n', ' ')
            extracted_comments.append(f"Comment from {author}: {content}")

        if extracted_comments:
            print(f"   -> Found {len(extracted_comments)} comments.")
        else:
            print("   -> No comments found.")

    except Exception as e:
        print(f"❌ Warning: Could not fetch comments. Error: {e}")

    return {
        "text": extracted_text,
        "image_paths": image_paths,
        "comments": "\n".join(extracted_comments)
    }


def enrich_context_from_links(main_gdoc_text: str) -> dict:
    """
    Finds all URLs in a text, fetches their content (recursively for Google Docs),
    and combines everything.
    """
    all_urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', main_gdoc_text)

    # --- Filter out ignored domains ---
    ignored_domains = ["jira", "atlassian.net", "emojipedia"]
    urls_to_process = [url for url in all_urls if not any(domain in url for domain in ignored_domains)]

    ignored_count = len(all_urls) - len(urls_to_process)
    if ignored_count > 0:
        print(f"   -> 🚫 Ignored {ignored_count} link(s) containing {ignored_domains}.")

    if not urls_to_process:
        print("ℹ️ No processable links found after filtering. Proceeding with original text.")
        return {
            "main_text": main_gdoc_text,
            "nested_text": "",
            "comments": ""
        }

    print(f"🔗 Processing {len(urls_to_process)} links...")

    # Separate Google Doc links from other web pages
    google_doc_urls = [url for url in urls_to_process if "docs.google.com/document" in url]
    external_urls = [url for url in urls_to_process if "docs.google.com/document" not in url]

    all_fetched_text = ""
    all_comments = []

    # --- Process Google Doc Links (Non-Recursive) ---
    for url in google_doc_urls:
        # Extract the document ID from the URL
        match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
        if match:
            doc_id = match.group(1)
            print(f"\n--- Fetching Google Doc: {doc_id[:15]}... ---")
            nested_doc_assets = read_google_doc_multimodal(doc_id)
            if nested_doc_assets:
                all_fetched_text += f"\n\n--- CONTENT FROM LINKED DOC: {url} ---\n\n"
                all_fetched_text += nested_doc_assets["text"]
                all_comments.append(nested_doc_assets["comments"])

    # --- Process other external links ---
    if external_urls:
        print(f"\n--- Fetching {len(external_urls)} external web pages... ---")
        try:
            documents_from_urls = SimpleWebPageReader(html_to_text=True).load_data(external_urls)
            all_fetched_text += "\n\n--- LINKED EXTERNAL CONTENT ---\n\n".join([doc.text for doc in documents_from_urls])
        except Exception as e:
            print(f"❌ Warning: Could not fetch content from some external links. Error: {e}")

        # Combine comments into a single string
    combined_comments = "\n".join(all_comments)

    print("\n✅ Successfully enriched context.")
    return {
        "main_text": main_gdoc_text,
        "nested_text": all_fetched_text,
        "comments": combined_comments
    }


def generate_key_high_level_idea_for_gdoc(technical_document_text: str):
    model_name = "gemini-2.0-flash-001"
    model = ChatVertexAI(
        model_name=model_name,
        project=PROJECT_ID,
        location=LOCATION,
    )

    prompt_template = GDOC_GENERATE_KEY_HIGH_LEVEL_IDEA
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 3. Define the output parser
    # This simply takes the model's message content and returns it as a string.
    output_parser = StrOutputParser()

    # 4. Create the LangChain "chain"
    # This links the prompt, model, and output parser together.
    chain = prompt | model | output_parser
    result_text = chain.invoke({"technical_document_text": technical_document_text})

    # Parse the text output into a dictionary
    idea_dict = {}
    for line in result_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            idea_dict[key.strip()] = value.strip()

    print(f"""--- Blog Idea Variables ---
    Title: {idea_dict.get("Title")}
    Target Audience: {idea_dict.get("Audience")}
    Key Takeaway: {idea_dict.get("Takeaway")}
    Summary for Kapa AI: {idea_dict.get("KapaAIinput")}
    --------------------------""")

    return idea_dict


def extract_doc_id_from_url(url: str) -> str | None:
    """
    Extracts the Google Doc ID from a URL using a regular expression.
    """
    # The regex looks for the string between '/d/' and the next '/'
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    return None


# --- Example Main Execution ---
if __name__ == "__main__":
    # DOC_ID = "1ye31HS5vHhlYJbXcT3HPc0q1I4hN7OviG90C0bvbl-A"
    DOC_ID = "1g3FK4f6tuGcDBC2YXmPjQEKr1SB1y_CTe-EXZfTQX-U"

    # Get text, images, and comments from the Google Doc
    document_assets = read_google_doc_multimodal(DOC_ID)

    if document_assets:
        print("\n--- Extracted Text (Snippet) ---")
        print(document_assets["text"][:300] + "...")

        print("\n--- Downloaded Images ---")
        print(document_assets["image_paths"])

        print("\n--- Extracted Comments ---")
        print(document_assets["comments"])

        enriched_text = enrich_context_from_links(document_assets["text"])

        # Now you can combine these assets to create a rich context for Gemini
        # full_context = f"DOCUMENT TEXT:\n{document_assets['text']}\n\nDISCUSSION FROM COMMENTS:\n{document_assets['comments']}"
        # print("\n--- Full Context for AI ---")
        # print(full_context)
