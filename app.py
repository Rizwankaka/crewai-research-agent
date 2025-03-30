import os
import sys

# Force simplified approach for Streamlit Cloud deployment
# This bypasses the SQLite/ChromaDB dependency issues
FORCE_SIMPLIFIED = True  # Change to False to use CrewAI locally

# Set environment variables to disable problematic dependencies
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""
os.environ["CREWAI_DISABLE_CHROMA"] = "true"
os.environ["IS_STREAMLIT_CLOUD"] = "true"
os.environ["DISABLE_CHROMADB"] = "true"
os.environ["USE_SIMPLIFIED_MODE"] = "true"

import streamlit as st
from src.ui import (
    setup_page_config,
    render_header,
    render_sidebar,
    show_result
)
from src.utils import load_environment, get_api_key

# Initialize session state
if 'gemini_api_key' not in st.session_state:
    st.session_state['gemini_api_key'] = None
if 'serper_api_key' not in st.session_state:
    st.session_state['serper_api_key'] = None
if 'topic' not in st.session_state:
    st.session_state['topic'] = None

# Load environment variables
load_environment()

# Configure page
setup_page_config()

# Render header with animations and title
render_header()

# Render sidebar with controls and collect input values
topic, gemini_api_key, serper_api_key, temperature, generate_button = render_sidebar()

# Save topic to session state for filename creation
if topic:
    st.session_state['topic'] = topic

# Main content area
if generate_button:
    # Validate inputs
    if not topic:
        st.error("⚠️ Please enter a topic to generate content about.")
    elif not gemini_api_key:
        st.error("⚠️ Please enter your GEMINI API key.")
    elif not serper_api_key and not FORCE_SIMPLIFIED:
        # Only require Serper API key for local environment with CrewAI
        st.error("⚠️ Please enter your SERPER API key for web research.")
    else:
        # Set up the environment variables for the API keys
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        if serper_api_key:
            os.environ["SERPER_API_KEY"] = serper_api_key
        
        with st.spinner('🔍 AI agents are researching and writing content... This may take a few minutes.'):
            if FORCE_SIMPLIFIED:
                try:
                    # Skip CrewAI and SQLite entirely - use direct Gemini API
                    from src.utils.simplified_generator import generate_simple_content
                    st.info("Using simplified content generator for cloud deployment...")
                    result = generate_simple_content(topic, gemini_api_key)
                    show_result(result)
                except Exception as e:
                    st.error(f"🚨 Error generating content: {str(e)}")
            else:
                # Try to use CrewAI approach for local environment
                try:
                    # Import ResearchCrew here to avoid initialization issues with SQLite
                    from src.agents import ResearchCrew
                    
                    # Initialize the research crew and generate content
                    research_crew = ResearchCrew(
                        topic=topic, 
                        model="gemini/gemini-2.0-flash", 
                        temperature=temperature
                    )
                    
                    # Generate content with the provided API key
                    result = research_crew.generate_content(serper_api_key=serper_api_key)
                    
                    # Show the result
                    show_result(result)
                    
                except Exception as e:
                    error_message = str(e).lower()
                    if "sqlite" in error_message or "chroma" in error_message:
                        st.error(f"🚨 SQLite/ChromaDB compatibility error. Switching to simplified mode.")
                        
                        try:
                            from src.utils.simplified_generator import generate_simple_content
                            result = generate_simple_content(topic, gemini_api_key)
                            show_result(result)
                        except Exception as fallback_error:
                            st.error(f"Could not generate content: {str(fallback_error)}")
                    
                    elif "serper" in error_message:
                        st.error(f"🚨 Error with Serper API: {str(e)}")
                        st.warning("""
                            #### Serper API Issue Detected
                            The Serper search tool failed. This might be due to:
                            - Invalid Serper API key
                            - Exceeded API usage limits
                            - Network connectivity issues
                        """)
                        try:
                            from src.utils.simplified_generator import generate_simple_content
                            st.info("🔄 Attempting to generate content without web search...")
                            result = generate_simple_content(topic, gemini_api_key)
                            show_result(result)
                        except Exception as fallback_error:
                            st.error(f"🚨 Could not generate content: {str(fallback_error)}")
                    else:
                        st.error(f"🚨 An error occurred: {str(e)}")
                        st.markdown("""
                            #### Troubleshooting tips:
                            - Check if your API keys are valid
                            - Make sure your topic is clear and specific
                            - Try again with a different topic
                        """)

# Display a placeholder for content if no generation has been started
else:
    st.markdown(
        """
        <div style="text-align: center; padding: 50px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0; color: #333333;">
            <img src="https://img.icons8.com/fluency/96/000000/light-on.png" width="80"/>
            <h3 style="color: #333333;">Enter a topic and click "Generate Content" to start!</h3>
            <p style="color: #333333;">Our AI agents will research and write content about any topic you're interested in.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Example topics section
    st.markdown("### 💡 Example Topics to Try")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; text-align: center;">
                <p><strong>The Future of Quantum Computing</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; text-align: center;">
                <p><strong>Sustainable Urban Development</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; text-align: center;">
                <p><strong>Advancements in AI Ethics</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>Built with <a href="https://www.crewai.io/" target="_blank">CrewAI</a>, <a href="https://streamlit.io/" target="_blank">Streamlit</a> and ❤️ by <a href="https://github.com/Rizwankaka" target="_blank">Rizwan Rizwan</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
