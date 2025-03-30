import os
import sys

# No CrewAI or ChromaDB imports at all in the main file when deployed
# We'll only import the simplified generator and UI components

import streamlit as st
from src.ui import (
    setup_page_config,
    render_header,
    render_sidebar,
    show_result
)
from src.utils import load_environment, get_api_key
from src.utils.simplified_generator import generate_simple_content

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
    else:
        # Set up the environment variables for the API keys
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        if serper_api_key:
            os.environ["SERPER_API_KEY"] = serper_api_key
        
        with st.spinner('🔍 AI agents are researching and writing content... This may take a few minutes.'):
            try:
                # Use simplified generator for all deployments
                st.info("Using content generator optimized for cloud deployment...")
                result = generate_simple_content(topic, gemini_api_key)
                show_result(result)
            except Exception as e:
                st.error(f"🚨 Error generating content: {str(e)}")
                st.markdown("""
                    #### Troubleshooting tips:
                    - Check if your GEMINI API key is valid
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
