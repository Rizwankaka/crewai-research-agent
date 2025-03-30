# Use lazy loading to avoid importing problematic dependencies at startup
# This prevents the SQLite version check from running on module import

import os
import sys
import importlib

# Define a function to check if we're in Streamlit Cloud
def is_streamlit_cloud():
    """Check if running in Streamlit Cloud environment"""
    return os.environ.get('IS_STREAMLIT_CLOUD', '') == 'true' or os.getenv('STREAMLIT_RUNTIME', '') != ''

# Define a lazy-loading class to avoid direct import
class LazyResearchCrew:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            # Only load the actual class when first accessed
            if not is_streamlit_cloud():
                try:
                    module = importlib.import_module('.research_crew', package='src.agents')
                    cls._instance = module.ResearchCrew
                except ImportError as e:
                    print(f"Failed to import ResearchCrew: {e}")
                    from src.utils.simplified_generator import generate_simple_content
                    cls._instance = None
            else:
                cls._instance = None
        return cls._instance or DummyResearchCrew

# Define a dummy class for environments where CrewAI can't be used
class DummyResearchCrew:
    def __init__(self, topic, model=None, temperature=None):
        self.topic = topic
        
    def generate_content(self, serper_api_key=None):
        from src.utils.simplified_generator import generate_simple_content
        return generate_simple_content(self.topic, os.environ.get("GEMINI_API_KEY", ""))

# Define a new getter that will return the appropriate class
def get_research_crew():
    """Get the appropriate ResearchCrew implementation based on environment"""
    loader = LazyResearchCrew()
    return loader() if callable(loader) else DummyResearchCrew

# Export only the getter function to avoid direct imports
ResearchCrew = get_research_crew()