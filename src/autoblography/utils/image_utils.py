"""
Image generation utilities using Vertex AI Imagen and Mermaid.js
"""

import os
import random
import subprocess
from typing import List, Dict, Any

import vertexai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from vertexai.preview.vision_models import ImageGenerationModel

from ..config.settings import settings


def generate_image_from_prompt_imagen(prompt_text: str, output_filename: str) -> None:
    """
    Generates an image using Imagen on Vertex AI based on a text prompt.
    
    Args:
        prompt_text: Text prompt for image generation
        output_filename: Output filename for the generated image
    """
    print(f"🎨 Generating image for prompt: {prompt_text}'...")

    # Initialize the connection to Vertex AI
    vertexai.init(project=settings.google_project_id, location=settings.google_location)

    # Load the image generation model
    model = ImageGenerationModel.from_pretrained("imagen-4.0-fast-generate-preview-06-06")

    # Generate the image
    response = model.generate_images(
        prompt=prompt_text,
        negative_prompt="noisy, overlapped text, clutter, complex background, messy text, spelling mistakes, confusing arrows",
        number_of_images=1,
        guidance_scale=10.0,  # optional, controls creativity
        aspect_ratio=random.choice(["1:1", "4:3", "3:4"])
    )

    # Save the image
    response.images[0].save(output_filename)
    print(f"✅ Image saved as {output_filename}")


def generate_image_from_mermaid(prompt_text: str, output_filename: str) -> None:
    """
    Generates an image using Mermaid.js based on a text prompt.
    
    Args:
        prompt_text: Text prompt for diagram generation
        output_filename: Output filename for the generated image
    """
    temp_mmd_file = f"mmd_file_{output_filename}.mmd"
    output_filename_svg = f"{output_filename}.svg"
    prompt_text = f"This should be a flat vector-style schematic diagram in SVG style. {prompt_text}"
    print(f"🎨 Generating image for Mermaid prompt: {prompt_text}'...")

    # Use gemini-2.5-pro for complex image generation tasks
    model = ChatVertexAI(
        model_name="gemini-2.5-pro",
        project=settings.google_project_id,
        location=settings.google_location,
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

    print(f"🤖 Processing prompt with {settings.vertex_ai_model}...")
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
        
        # Clean up temporary file
        os.remove(temp_mmd_file)
        
    except FileNotFoundError:
        print("❌ Error: 'mmdc' command not found. Is the Mermaid CLI installed?")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error rendering SVG: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def generate_images(blog_assets: Dict[str, Any]) -> str:
    """
    Processes blog assets by generating images from prompts and replacing placeholders
    in the blog content with Markdown image syntax.

    Args:
        blog_assets: A dictionary containing blog content and image prompts.

    Returns:
        The blog content with placeholders replaced by Markdown image syntax.
    """
    blog_content = blog_assets.get("blog_markdown_content", "")
    image_prompts = blog_assets.get("image_prompts", [])
    
    # Create images directory if it doesn't exist
    os.makedirs(settings.image_output_dir, exist_ok=True)
    
    # Generate images for each prompt
    for i, image_prompt in enumerate(image_prompts):
        placeholder = image_prompt.get("placeholder")
        prompt = image_prompt.get("prompt")
        
        if placeholder and prompt:
            # Generate unique filename
            image_filename = f"blog_image_{i+1}.png"
            image_path = os.path.join(settings.image_output_dir, image_filename)
            
            try:
                # Generate image using Imagen
                generate_image_from_prompt_imagen(prompt, image_path)
                
                # Replace placeholder with markdown image syntax
                markdown_image = f"![{prompt[:50]}...]({image_path})"
                blog_content = blog_content.replace(placeholder, markdown_image)
                
            except Exception as e:
                print(f"❌ Error generating image for {placeholder}: {e}")
                # Replace placeholder with a note about the missing image
                blog_content = blog_content.replace(placeholder, f"*[Image generation failed: {e}]*")
    
    return blog_content 