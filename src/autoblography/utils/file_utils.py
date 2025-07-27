"""
File utilities for saving and converting documents
"""

import pypandoc
from typing import Dict, Any

# Download pandoc for document conversion
pypandoc.download_pandoc()


def save_markdown_as_word(filename: str, markdown_content: str) -> None:
    """
    Converts a string of Markdown text into a formatted .docx file.
    
    Args:
        filename: Output filename for the Word document
        markdown_content: Markdown content to convert
    """
    print(f"📄 Converting Markdown to Word document: {filename}...")

    # Convert the markdown string to a .docx file
    pypandoc.convert_text(
        markdown_content, 
        'docx', 
        format='markdown_strict', 
        outputfile=filename
    )

    print(f"✅ Successfully saved to {filename}")


def save_markdown_file(filename: str, markdown_content: str) -> None:
    """
    Saves markdown content to a .md file.
    
    Args:
        filename: Output filename for the markdown file
        markdown_content: Markdown content to save
    """
    print(f"📄 Saving Markdown file: {filename}...")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Successfully saved to {filename}") 