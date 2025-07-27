import random
import subprocess

import vertexai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from vertexai.preview.vision_models import ImageGenerationModel

# --- Configuration ---
PROJECT_ID = "hackathon-2025-463220"
LOCATION = "us-central1"


def generate_image_from_prompt_imagen(prompt_text: str, output_filename: str):
    """
    Generates an image using Imagen on Vertex AI based on a text prompt.
    """
    print(f"🎨 Generating image for prompt: {prompt_text}'...")

    # Initialize the connection to Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Load the image generation model
    model = ImageGenerationModel.from_pretrained("imagen-4.0-fast-generate-preview-06-06")
    # model = ImageGenerationModel.from_pretrained("imagen-4.0-ultra-generate-preview-06-06")

    # Generate the image
    response = model.generate_images(
        prompt=prompt_text,
        negative_prompt="noisy, overlapped text, clutter, complex background, messy text, spelling mistakes, confusing arrows",
        number_of_images=1,
        guidance_scale=10.0,  # optional, controls creativity
        aspect_ratio=random.choice(["1:1", "4:3", "3:4"])
    )

    # Save the image
    response.images[0].save(f"{output_filename}")
    print(f"✅ Image saved as {output_filename}")


def generate_image_from_mermaid(prompt_text: str, output_filename: str):
    """
    Generates an image using Mermaid.js based on a text prompt.
    """
    temp_mmd_file = f"mmd_file_{output_filename}.mmd"
    output_filename_svg = f"{output_filename}.svg"
    prompt_text = f"This should be a flat vector-style schematic diagram in SVG style. {prompt_text}"
    print(f"🎨 Generating image for Mermaid prompt: {prompt_text}'...")

    # This function is a placeholder for actual Mermaid.js integration
    # In practice, you would need to render the Mermaid diagram and save it as an image
    # Here we just simulate saving an image

    model_name = "gemini-2.5-pro"
    model = ChatVertexAI(
        model_name=model_name,
        project=PROJECT_ID,
        location=LOCATION,
    )

    prompt_template = f"""
        **ROLE AND GOAL:**
        You are a senior expert in creating diagrams using Mermaid.js syntax. Your sole purpose is to convert a user's textual description into clean, valid, and well-structured Mermaid code. No syntax error should be made.

        **TASK: GENERATE MERMAID CODE**
        Analyze the user's request below and generate the corresponding Mermaid code.

        **STRICT OUTPUT RULES:**
        - **ONLY** output the raw Mermaid code block.
        - Do **NOT** include any explanations, apologies, or introductory text like "Here is the code:".
        - Do **NOT** enclose the code in Markdown backticks (```mermaid ... ```).
        - Ensure the generated code is immediately ready for rendering.

        **HERE IS THE USER'S REQUEST:**
        "{prompt_text}"
        """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    print(f"🤖 Processing prompt with {model}...")
    mermaid_code = chain.invoke({"prompt_text": prompt_text})
    print("\n--- GENERATED MERMAID CODE ---")
    print(mermaid_code)
    try:
        with open(temp_mmd_file, "w") as f:
            f.write(mermaid_code)

        print(f"\n🎨 Rendering SVG to '{output_filename_svg}'...")
        subprocess.run(
            ["mmdc", "-i", temp_mmd_file, "-o", output_filename_svg],
            check=True,
            capture_output=True  # Hides CLI output unless there's an error
        )
        print("✅ SVG file created successfully!")
    except FileNotFoundError:
        print("❌ Error: 'mmdc' command not found. Is the Mermaid CLI installed?")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during SVG rendering: {e.stderr.decode()}")


# --- Main Execution ---
if __name__ == "__main__":
    # This is the descriptive prompt that your main script would generate
    blog_image_prompt = "A simple 2D schematic diagram of a YugabyteDB tiered storage architecture. The diagram should show a large box labeled 'YugabyteDB Universe'. Inside this universe, there are two distinct groups of nodes. The left group is labeled 'Hot Tier' and contains three nodes depicted as servers with 'SSD' written on them. The right group is labeled 'Cold Tier' and contains three nodes depicted as servers with 'HDD' written on them. An arrow from an icon labeled 'Application' points to the 'Hot Tier' with the text 'Low-latency reads/writes for recent data'. Another arrow from the 'Application' icon points to the 'Cold Tier' with the text 'Queries for historical data'"

    # Call the function to generate and save the image
    generate_image_from_prompt_imagen(
        prompt_text=blog_image_prompt,
        output_filename="blog_architecture_diagram"
    )

    # generate_image_from_mermaid(
    #     prompt_text=blog_image_prompt,
    #     output_filename="blog_architecture_diagram.svg"
    # )
