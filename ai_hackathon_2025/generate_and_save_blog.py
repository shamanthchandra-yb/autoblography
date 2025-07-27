import json
import os
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pypandoc

from ai_hackathon_2025.image_generation import generate_image_from_prompt_imagen, generate_image_from_mermaid
from ai_hackathon_2025.prompt_constant import SLACK_GENERATE_STRUCTURED_BLOG_ASSETS, GDOC_GENERATE_STRUCTURED_BLOG_ASSETS

pypandoc.download_pandoc()

# --- Configuration ---
PROJECT_ID = "hackathon-2025-463220"
LOCATION = "us-central1"
os.environ["GCLOUD_PROJECT"] = PROJECT_ID
# model_name = "gemini-2.0-flash-001"
model_name = "gemini-2.5-pro"


def save_markdown_as_word(filename: str, markdown_content: str):
    """
    Converts a string of Markdown text into a formatted .docx file.
    """
    print(f"📄 Converting Markdown to Word document: {filename}...")

    # Convert the markdown string to a .docx file
    pypandoc.convert_text(markdown_content, 'docx', format='markdown_strict', outputfile=filename)

    print(f"✅ Successfully saved to {filename}")


# --- Main Blog Generation Function ---
def generate_structured_blog_assets(source_type: str, source_data, documentation_links: list[tuple[str, str]]):
    """
    Generates a full blog post and saves it to a Word file.
    """
    print(f"Generating blog post'...")
    model = ChatVertexAI(model_name=model_name, project=PROJECT_ID, location=LOCATION)
    prompt_template = ""

    if source_type == "slack":
        prompt_template = SLACK_GENERATE_STRUCTURED_BLOG_ASSETS
        invoke_input = {
            "conversation_text": source_data,
            "documentation_links": json.dumps(documentation_links)
        }
    elif source_type == "gdoc":
        prompt_template = GDOC_GENERATE_STRUCTURED_BLOG_ASSETS
        invoke_input = {
            "main_document_text": source_data["main_text"],
            "linked_documents_content": source_data["nested_text"],
            "document_comments": source_data["comments"],
            "documentation_links": json.dumps(documentation_links)
        }
    else:
        raise ValueError("Invalid source_type. Must be 'slack' or 'gdoc'.")

    prompt = ChatPromptTemplate.from_template(prompt_template)
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    # Generate the blog content
    raw_response = chain.invoke(invoke_input)
    # --- ADD THIS ROBUST PARSING LOGIC ---

    print("\n--- Raw AI Response ---")
    print(raw_response)
    print("-----------------------\n")

    try:
        # Find the first '{' and the last '}' to isolate the JSON object
        start_index = raw_response.find('{')
        end_index = raw_response.rfind('}') + 1

        if start_index == -1 or end_index == 0:
            raise json.JSONDecodeError("Could not find a JSON object in the response.", raw_response, 0)

        # Extract only the JSON part of the string
        json_string = raw_response[start_index:end_index]

        # Parse the extracted JSON string
        structured_output = json.loads(json_string)
        return structured_output

    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Failed to parse JSON from the AI's response. Reason: {e}")
        return None


def add_blog_assets(blog_assets: dict) -> str:
    """
    Processes blog assets by generating images from prompts and replacing placeholders
    in the blog content with Markdown image syntax.

    Args:
        blog_assets (dict): A dictionary containing blog content and image prompts.

    Returns:
        str: The blog content with placeholders replaced by Markdown image syntax.
    """
    if not blog_assets:
        return ""

    print("\n✅ Successfully received structured data from AI!")

    blog_content_with_placeholders = blog_assets.get("blog_markdown_content", "")
    image_prompts = blog_assets.get("image_prompts", [])

    for i, img_data in enumerate(image_prompts):
        placeholder = img_data.get("placeholder")
        prompt = img_data.get("prompt")
        image_filename = f"blog_image_{i + 1}.png"

        print(f"\n--- Processing Image {i + 1} ---")
        generate_image_from_prompt_imagen(prompt, image_filename)
        # generate_image_from_mermaid(prompt, image_filename)

        # Replace the placeholder with the Markdown syntax for the local image
        blog_content_with_placeholders = blog_content_with_placeholders.replace(
            placeholder,
            f"![]({image_filename})"
        )

    return blog_content_with_placeholders
