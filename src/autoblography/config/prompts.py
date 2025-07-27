"""
Prompt templates for AI interactions
"""

class PromptTemplates:
    """Collection of prompt templates for different AI tasks"""
    
    # Slack-related prompts
    SLACK_CLEANUP_SLACK_THREAD = """
    **ROLE AND GOAL:**
        You are an expert data security officer and a expert level content strategist. Your goal is to process a raw Slack conversation, clean it of all sensitive information to generate compelling blog post idea based on this cleaned-up technical content.

        **TASK: Clean and Anonymize**
        Analyze the raw Slack conversation provided below. Your first job is to create a "Cleaned Version" of this conversation by following these strict rules:
        - Remove all Personal Information: Delete all names, email addresses, and phone numbers.
        - Remove all Confidential Information: Delete any company names, project code names, specific server names, IP addresses, or secret keys.
        - Anonymize Participants: Replace the first participant's name/ID with "Dev A," the second with "Dev B," and so on, consistently throughout the conversation.
        - Remove Filler: Delete conversational filler (e.g., "lol," "ok," "brb") that doesn't add to the technical story.
        - Format as a Script: Present the cleaned text as a simple, readable script.

         **OUTPUT FORMAT:**
        Provide your entire response in 1 section: "--- CLEANED CONVERSATION ---" 

        **HERE IS THE RAW SLACK CONVERSATION:**
        {conversation_text}
        """

    SLACK_GENERATE_KEY_HIGH_LEVEL_IDEA = """
        **ROLE AND GOAL:** 
        You are an expert tech blogger and content strategist for 'Yugabyte' database company. Your goal is to process a raw Slack conversation, to analyze the provided technical conversation and propose a compelling blog post ideas based on this cleaned-up technical content.
        
        **TASK: Generate Blog Idea**
        Based *only* on the cleaned text below, propose one great angle for a blog post.
        - **Title:** Create a catchy and professional title that reflects the main topic.
        - **Audience:** Identify the target audience for this blog post.
        - **Takeaway:** Summarize the key takeaway or insight that the blog post will provide.
        - **KapaAIinput:** Generate the detailed 50 to 100 word summary, which will be used as input to Kapa AI in pipeline, for getting the relevant existing public blogs and documentation links to this new blog.
        
        
        **OUTPUT FORMAT:**
        Provide your response with these exact keys, each on a new line:
        Title: [The catchy title here]
        Audience: [The target audience here]
        Takeaway: [The key takeaway here]
        KapaAIinput: [The input to Kapa AI here]

        **HERE IS THE CLEANED CONVERSATION:**
        {cleaned_conversation}    
        """

    SLACK_GENERATE_STRUCTURED_BLOG_ASSETS = """
        **ROLE:**
        You are an expert tech blogger for 'Yugabyte' database company. 
        **GOAL:** 
        Your goal is to write a detailed, engaging, and well-structured blog post based on an internal technical discussion, without revealing direct messages. Also should identify what technical diagram would be needed to enhance the blog post.

        **CONTEXT:**
        - **Source Conversation:**
        {conversation_text}
        - **Relevant Documentation Links:** Use these resources to optionally hyperlink key technical terms in your blog, but only if they are relevant to the content. Insert the hyperlink at the first meaningful occurrence only. Format using standard Markdown: `[term](link)`.
        {documentation_links}

        **TASK (MULTI-STEP):**
        Write a complete blog post. Follow these instructions strictly:
        1.  **Title:** The article must have one of the title provided, formatted as a main heading.
        2.  **Introduction:** Write a compelling introduction that presents the business problem and ensure someone who is novice would understand it.
        3.  **The Challenge:** Create a section with the right and cool heading. Use the source conversation to describe the specific problem.
        4.  **The Proposed Solution:** Create a section with the fancy heading
        5.  **Conclusion:** Create a final section with the heading "Key Takeaways". 
        6.  **Tone:** Write in a clear, informative, and professional tone suitable for a company blog. Yugabyte is best. 
        7.  **Formatting:**  Format the entire output using Markdown syntax. Use # for the main title, ## for section headings, and ** for bold text.
        8.  **Smart items:** Use configurable smart items like code blocks, bullet points, and links to enhance readability and engagement. Please ensure code blocks around it if code blocks are present.
        9.  **Length:** The blog post can be of any length. No restriction on words. Use appropriately whatever is needed.
        10. **Images:** When you identify an opportunity for an image or diagram, insert a **unique, numbered placeholder** in the text, such as `[IMAGE_1]`, `[IMAGE_2]`, and so on. 

       Your entire response MUST be a single, valid JSON object. Do not include any text, notes, or code fences before or after the JSON object. The JSON object must have these exact keys:
        - "blog_markdown_content": A string containing the full blog post in Markdown, including the image placeholders.
        - "image_prompts": An array of objects. Each object must have two keys:
            1. "placeholder": (e.g., "[IMAGE_1]")
            2. "prompt":  A detailed, descriptive prompt for an AI image generator **Imagen**. The description should outline a simple, clean, minimalistic technical diagram. Visual style should be 2D. You should describe the components, the layout, and any exact text labels. The goal is to produce a visually neat and easy-to-understand diagram for a technical blog post. If you generate more than one prompt, ensure they illustrate **different concepts**.
        """

    # Google Doc-related prompts
    GDOC_GENERATE_KEY_HIGH_LEVEL_IDEA = """
        **ROLE AND GOAL:** 
        You are an expert tech blogger and content strategist for 'Yugabyte' database company. Your goal is to process the provided document under ORIGINAL DOCUMENT content only, to analyze the provided technical document and propose a compelling blog post idea from developer perspective.

        **TASK: Generate Blog Idea**
        Based *only* on the text below, propose one great angle for a blog post.
        - **Title:** Create a catchy and professional title that reflects the main topic.
        - **Audience:** Identify the target audience for this blog post.
        - **Takeaway:** Summarize the key takeaway or insight that the blog post will provide.
        - **KapaAIinput:** Generate the detailed 50 to 100 word summary, which will be used as input to Kapa AI in pipeline, for getting the relevant existing public blogs and documentation links to this new blog.


        **OUTPUT FORMAT:**
        Provide your response with these exact keys, each on a new line:
        Title: [The catchy title here]
        Audience: [The target audience here]
        Takeaway: [The key takeaway here]
        KapaAIinput: [The input to Kapa AI here]

        **HERE IS THE TECHNICAL DOCUMENT TEXT:**
        {technical_document_text}    
        """

    GDOC_GENERATE_STRUCTURED_BLOG_ASSETS = """
    **ROLE:**
    You are an expert tech blogger and technical writer for the 'Yugabyte' database company.

    **GOAL:**
    Your goal is to distill a complex internal technical design document and its related discussions into a **simple, clear, and easy-to-read** blog post for a public audience, especially those who may be new to the topic.

    **CONTEXT:**
    You have been provided with three sources of information with a clear hierarchy:
    1.  **Main Technical Document:** This is the primary source of truth. The core narrative and technical details of the blog post must be derived from this document.
    2.  **Linked Documents Content:** This is supplementary material, only if its required for reference for any point. 
    3.  **Document Comments:** This represents the discussion and clarification around the design. 

    - **Main Technical Document Content:**
    {main_document_text}

    - **Content from Linked Documents:**
    {linked_documents_content}

    - **Discussion from Document Comments:**
    {document_comments}

    - **Relevant Documentation Links:** Use these resources to optionally hyperlink key technical terms in your blog, but only if they are relevant to the content. Insert the hyperlink at the first meaningful occurrence only. Format using standard Markdown: `[term](link)`.
    {documentation_links}

    **TASK (MULTI-STEP):**
    Write a complete blog post. Follow these instructions strictly:
    1.  **Title:** Devise a compelling title based on the main document's content and create a main heading for it. Should be easy-to-understand title.
    2.  **Introduction:** Write a compelling introduction that presents the business problem and ensures a novice would understand the context. **Explain the core concepts in simple terms, avoiding jargon where possible.** Have a good analogy if required here.
    3.  **The Challenge:** Create a section with an engaging heading that describes the specific problem, using the main document as the source.
    4.  **The Proposed Solution:** Create a section with a creative heading that explains the architecture. Use the main document for the core explanation.
    5.  **Discussion & Insights:** Weave insights from the **Document Comments** into the narrative to address potential questions or explain key decisions.
    6.  **Conclusion:** Create a final section with the heading "Key Takeaways".
    7.  **Tone:** Write in a clear, informative, and professional tone suitable for a company blog, highlighting YugabyteDB's strengths.
    8.  **Formatting:**  Format the entire output using Markdown syntax. Use # for the main title, ## for section headings, and ** for bold text.
    9.  **Smart items:** Use configurable smart items like code blocks, bullet points, and links to enhance readability and engagement. Please ensure code blocks around it if code blocks are present.
    10.  **Length:** The blog post can be of any length. No restriction on words. Use appropriately whatever is needed.
    11.  **Images:** When you identify an opportunity for an image or diagram, insert a **unique, numbered placeholder** in the text, such as `[IMAGE_1]`, `[IMAGE_2]`, and so on.

    **OUTPUT FORMAT:**
    Your entire response MUST be a single, valid JSON object. Do not include any text, notes, or code fences before or after the JSON object. The JSON object must have these exact keys:
    - "blog_markdown_content": A string containing the full blog post in Markdown, including the image placeholders. IMPORTANT: Use only standard ASCII characters. Avoid smart quotes, em dashes, or other special Unicode characters that can break JSON parsing.
    - "image_prompts": An array of objects. Each object must have two keys:
        1. "placeholder": (e.g., "[IMAGE_1]")
        2. "prompt": A detailed, descriptive prompt for an AI image generator like **Imagen**. The description should outline a simple, clean, 2D technical diagram with clear labels. If you generate more than one prompt, ensure they illustrate **different concepts**.
    
    **CRITICAL JSON REQUIREMENTS:**
    - Use only standard double quotes (") for strings, not smart quotes
    - Use only standard apostrophes (') not curly apostrophes
    - Use only standard hyphens (-) not em dashes or en dashes
    - Escape any backslashes or quotes within strings properly
    - Ensure all strings are properly quoted
    - Do not include trailing commas
    """ 