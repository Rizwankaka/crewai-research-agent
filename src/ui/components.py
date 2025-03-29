import streamlit as st
from streamlit_lottie import st_lottie
import requests

def setup_page_config():
    """Configure the Streamlit page with title and layout"""
    st.set_page_config(
        page_title="AI Research & Content Writer",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_lottie(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def render_header():
    """Render the app header with animations and title"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        lottie_animation = load_lottie("https://assets2.lottiefiles.com/packages/lf20_kuhijlvx.json")
        if lottie_animation:
            st_lottie(lottie_animation, height=150, key="header_animation1")
    
    with col2:
        st.title("🤖 AI Research & Content Writer")
        st.markdown(
            """
            <div style='text-align: center'>
                <h3>Powered by CrewAI</h3>
                <p>Generate well-researched blog posts on any topic using AI agents</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        lottie_animation2 = load_lottie("https://assets9.lottiefiles.com/packages/lf20_tno6uzqw.json")
        if lottie_animation2:
            st_lottie(lottie_animation2, height=150, key="header_animation2")
    
    st.markdown("<hr>", unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with all input controls and branding"""
    with st.sidebar:
        st.image("https://img.freepik.com/free-vector/artificial-intelligence-concept-circuit-board-background-with-robot-arm_1017-41025.jpg", use_container_width=True)
        
        st.header("✨ Content Settings")
        
        # API Key inputs with password masking
        gemini_api_key = st.text_input("GEMINI API Key", type="password", help="Enter your Google Gemini API key")
        if gemini_api_key:
            st.session_state['gemini_api_key'] = gemini_api_key
            
        serper_api_key = st.text_input("SERPER API Key", type="password", help="Enter your Serper API key for web search")
        if serper_api_key:
            st.session_state['serper_api_key'] = serper_api_key
        
        # Topic input
        topic = st.text_area(
            "📝 Enter your topic",
            height=120,
            placeholder="Enter the topic or question you want to research"
        )
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, help="Higher values make output more creative, lower values more deterministic")
        
        # Generate button
        generate_button = st.button(
            "🚀 Generate Content", 
            type="primary", 
            use_container_width=True
        )
        
        # Add help information
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. Enter your API keys (required for content generation)
            2. Type your desired content topic or question
            3. Adjust advanced settings if needed
            4. Click 'Generate Content'
            5. Wait for the AI research agents to work
            6. Download the result as a markdown file
            """)
        
        # Add branding with social links
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='text-align: center'>
                <h4>Created by Rizwan Rizwan</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                """<a href="https://github.com/Rizwankaka" target="_blank">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="30">
                </a>""", 
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """<a href="https://www.kaggle.com/rizwanrizwannazir" target="_blank">
                <img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/189_Kaggle_logo_logos-512.png" alt="Kaggle" width="30">
                </a>""", 
                unsafe_allow_html=True
            )
            
        with col3:
            st.markdown(
                """<a href="https://www.facebook.com/RIZWANNAZEEER" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/124/124010.png" alt="Facebook" width="30">
                </a>""", 
                unsafe_allow_html=True
            )
            
        with col4:
            st.markdown(
                """<a href="mailto:researcher@datafyassociates.com">
                <img src="https://cdn-icons-png.flaticon.com/512/281/281769.png" alt="Email" width="30">
                </a>""", 
                unsafe_allow_html=True
            )
    
    return topic, gemini_api_key, serper_api_key, temperature if 'temperature' in locals() else 0.7, generate_button

def show_result(result):
    """Display the generated content result"""
    # Save result in session state for sharing
    if 'generated_content' not in st.session_state:
        st.session_state['generated_content'] = result
    
    st.markdown("### 📄 Generated Content")
    
    with st.container():
        st.markdown(
            """
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; background-color: #f9f9f9;">
            """,
            unsafe_allow_html=True
        )
        st.markdown(result)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Create a sanitized filename - fix the issue that caused the error
    if 'topic' in st.session_state and st.session_state['topic']:
        # Remove any newlines and sanitize the topic for use as a filename
        topic_raw = st.session_state['topic']
        topic_filename = ''.join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in topic_raw)
        topic_filename = topic_filename.lower().replace(' ', '_')
        # Ensure no newlines or unsafe characters
        topic_filename = topic_filename.strip().replace('\n', '').replace('\r', '')
        # Limit filename length
        topic_filename = topic_filename[:50]
    else:
        topic_filename = "research_article"
    
    # Add download button with sanitized filename
    st.download_button(
        label="⬇️ Download as Markdown",
        data=result,
        file_name=f"{topic_filename}_article.md",
        mime="text/markdown",
        key="download_button"
    )
    
    # Add sharing options
    st.markdown("### Share this research")
    share_col1, share_col2, share_col3 = st.columns(3)
    
    # Copy to clipboard functionality
    with share_col1:
        if st.button("📤 Copy to Clipboard", key="copy_button"):
            try:
                # Use JavaScript to copy to clipboard
                js = f"""
                <script>
                    navigator.clipboard.writeText({repr(result)}).then(function() {{
                        alert("Content copied to clipboard!");
                    }})
                    .catch(function() {{
                        alert("Failed to copy. Please try again.");
                    }});
                </script>
                """
                st.components.v1.html(js, height=0)
                st.success("✅ Content copied to clipboard!")
            except Exception as e:
                st.error(f"Could not copy to clipboard: {str(e)}")
    
    # Email functionality
    with share_col2:
        if st.button("📧 Email Content", key="email_button"):
            topic_subject = st.session_state.get('topic', 'Research Article')
            email_subject = f"AI Research on: {topic_subject}"
            # Create a mailto link with the content
            email_body = "Here's the research article generated with AI:\n\n" + result[:1500] + "..."
            mailto_link = f"mailto:?subject={email_subject}&body={email_body}"
            
            # Open email client using JavaScript
            js = f"""
            <script>
                window.open('{mailto_link}', '_blank');
            </script>
            """
            st.components.v1.html(js, height=0)
            st.success("✅ Email client opened! If nothing happened, check your browser settings.")
    
    # Social media sharing functionality
    with share_col3:
        if st.button("📱 Share to Social", key="share_button"):
            # Create a collapsible section with sharing options
            with st.expander("Share to social media", expanded=True):
                st.markdown("#### Choose a platform to share")
                
                # Extract title from content or use topic
                title = topic_filename.replace('_', ' ').title()
                
                # Twitter/X button
                if st.button("𝕏 Share on Twitter/X"):
                    tweet_text = f"Check out this AI-generated research on {title}!"
                    twitter_url = f"https://twitter.com/intent/tweet?text={tweet_text}"
                    js = f"""
                    <script>
                        window.open('{twitter_url}', '_blank');
                    </script>
                    """
                    st.components.v1.html(js, height=0)
                    st.success("✅ Twitter/X sharing window opened!")
                
                # LinkedIn button
                if st.button("🔗 Share on LinkedIn"):
                    linkedin_url = "https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/Rizwankaka/crewai-research-agent"
                    js = f"""
                    <script>
                        window.open('{linkedin_url}', '_blank');
                    </script>
                    """
                    st.components.v1.html(js, height=0)
                    st.success("✅ LinkedIn sharing window opened!")
                
                # Facebook button
                if st.button("👥 Share on Facebook"):
                    facebook_url = "https://www.facebook.com/sharer/sharer.php?u=https://github.com/Rizwankaka/crewai-research-agent"
                    js = f"""
                    <script>
                        window.open('{facebook_url}', '_blank');
                    </script>
                    """
                    st.components.v1.html(js, height=0)
                    st.success("✅ Facebook sharing window opened!")