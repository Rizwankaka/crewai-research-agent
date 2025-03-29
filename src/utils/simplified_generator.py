import os
import google.generativeai as genai
import time

def generate_simple_content(topic, gemini_api_key):
    """
    Generate content without relying on CrewAI or ChromaDB
    This is a fallback for when SQLite version issues or other compatibility problems occur
    """
    if not gemini_api_key:
        return "Error: GEMINI API Key is required to generate content."

    try:
        # Configure the Gemini API
        genai.configure(api_key=gemini_api_key)
        
        # Set up the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",  # Using a more capable model for standalone generation
            generation_config={"temperature": 0.7}
        )
        
        # Create the research analyst prompt
        research_prompt = f"""
        You are a Senior Research Analyst. Your task is to research the topic: {topic}
        
        Please research and analyze this topic comprehensively, covering:
        1. Recent developments and news
        2. Key industry trends and innovations
        3. Expert opinions and analyses
        4. Statistical data and market insights
        
        Your research should:
        - Evaluate source credibility 
        - Fact-check all information
        - Include citations where possible
        - Be thorough and insightful
        
        Format your response as a detailed research brief with clear sections.
        """
        
        # Generate research content
        research_response = model.generate_content(research_prompt)
        research_text = research_response.text if hasattr(research_response, 'text') else str(research_response)
        
        # Add a small delay to avoid rate limiting
        time.sleep(2)
        
        # Create the content writer prompt using the research
        writer_prompt = f"""
        You are a skilled Content Writer. Your task is to transform the following research into an engaging blog post.
        
        RESEARCH BRIEF:
        {research_text}
        
        Please create a blog post that:
        1. Transforms technical information into accessible content
        2. Maintains all factual accuracy and citations from the research
        3. Includes:
           - Attention-grabbing introduction
           - Well-structured body sections with clear headings
           - Compelling conclusion
        4. Preserves all source citations in [Source: URL] format where available
        5. Includes a References section at the end
        
        Format your response as markdown with H1 for the title and H3 for sub-sections.
        """
        
        # Generate the final blog post
        final_response = model.generate_content(writer_prompt)
        final_content = final_response.text if hasattr(final_response, 'text') else str(final_response)
        
        return final_content
        
    except Exception as e:
        error_msg = str(e)
        
        # Create a fallback response when everything fails
        fallback_content = f"""
        # Research on {topic}
        
        ## Overview
        
        I apologize, but I encountered a technical issue while trying to generate comprehensive research on this topic.
        
        The specific error was: {error_msg}
        
        ## What you can do instead
        
        Since automated research couldn't be completed, here are some suggestions:
        
        1. Try again with a more specific topic
        2. Check that your API key is valid and has sufficient credits
        3. Try again later when the service might be more responsive
        
        ## Basic information
        
        While detailed research couldn't be performed, here's some general information about {topic}:
        
        * {topic} is an area worth exploring in depth
        * For more information, consider searching academic journals and news sources
        * Expert opinions can provide valuable insights on this topic
        
        Thank you for your understanding.
        """
        
        return fallback_content