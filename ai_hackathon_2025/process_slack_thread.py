import os
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Configuration ---
# Replace with your actual project ID and location
from ai_hackathon_2025.prompt_constant import SLACK_GENERATE_KEY_HIGH_LEVEL_IDEA, SLACK_CLEANUP_SLACK_THREAD

PROJECT_ID = "hackathon-2025-463220"
LOCATION = "us-west1"  # Or any other supported region

# Set the project for the gcloud library
os.environ["GCLOUD_PROJECT"] = PROJECT_ID


# --- Main Processing Function ---
def cleanup_slack_thread(raw_conversation: str):
    """
    Cleans a raw Slack conversation and generates blog post ideas using Gemini 1.5 Pro.
    """
    # 1. Initialize the Gemini 1.5 Pro model via LangChain
    # The 'stream=True' is good for interactive use, here we set it to False
    # to get the full response at once.
    model_name = "gemini-2.0-flash-001"
    model = ChatVertexAI(
        model_name=model_name,
        project=PROJECT_ID,
        location=LOCATION,
    )

    # 2. Define the prompt template for our combined task
    prompt_template = SLACK_CLEANUP_SLACK_THREAD

    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 3. Define the output parser
    # This simply takes the model's message content and returns it as a string.
    output_parser = StrOutputParser()

    # 4. Create the LangChain "chain"
    # This links the prompt, model, and output parser together.
    chain = prompt | model | output_parser

    # 5. Invoke the chain with the raw conversation
    print(f"🤖 Processing Slack conversation with {model_name}...")
    result = chain.invoke({"conversation_text": raw_conversation})

    return result


def generate_key_high_level_idea(cleaned_conversation: str):
    model_name = "gemini-2.0-flash-001"
    model = ChatVertexAI(
        model_name=model_name,
        project=PROJECT_ID,
        location=LOCATION,
    )

    prompt_template = SLACK_GENERATE_KEY_HIGH_LEVEL_IDEA
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 3. Define the output parser
    # This simply takes the model's message content and returns it as a string.
    output_parser = StrOutputParser()

    # 4. Create the LangChain "chain"
    # This links the prompt, model, and output parser together.
    chain = prompt | model | output_parser
    result_text = chain.invoke({"cleaned_conversation": cleaned_conversation})

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


def format_slack_data(slack_json_data: list) -> str:
    """
    Takes a list of Slack message objects (JSON/dictionaries) and formats
    it into a simple, readable string.
    """
    formatted_lines = []
    for message in slack_json_data:
        # We only care about actual user messages
        if message.get('type') == 'message' and message.get('user'):
            user_id = message['user']
            text = message.get('text', '')
            formatted_lines.append(f"From: {user_id}\n{text}\n")

    return "\n".join(formatted_lines)
