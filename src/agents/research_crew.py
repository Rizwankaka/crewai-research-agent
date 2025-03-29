import os
import sys
import platform

# Check if running in Streamlit Cloud environment
def is_streamlit_cloud():
    """Detect if running in Streamlit Cloud environment"""
    return os.environ.get('IS_STREAMLIT_CLOUD', '') == 'true' or os.getenv('STREAMLIT_RUNTIME', '') != ''

# Import conditionally based on environment
if is_streamlit_cloud():
    # Running in Streamlit Cloud - use simplified approach
    print("Detected Streamlit Cloud environment. Using simplified approach without ChromaDB dependency.")
    # Define dummy classes to prevent import errors
    class DummyCrew:
        def __init__(self, agents, tasks, verbose=True):
            self.agents = agents
            self.tasks = tasks
            self.verbose = verbose
        
        def kickoff(self, inputs):
            return "Error: CrewAI is not available in this environment due to SQLite compatibility issues."
    
    class DummyAgent:
        def __init__(self, role, goal, backstory, allow_delegation=False, verbose=True, tools=None, llm=None):
            self.role = role
            self.goal = goal
            self.backstory = backstory
    
    class DummyTask:
        def __init__(self, description, expected_output, agent):
            self.description = description
            self.expected_output = expected_output
            self.agent = agent
    
    Agent = DummyAgent
    Task = DummyTask
    Crew = DummyCrew
    LLM = lambda model, temperature: None
else:
    # Normal environment - import real classes
    try:
        from crewai import Agent, Task, Crew, LLM
    except ImportError:
        print("Error importing CrewAI. Please install with: pip install crewai")
        # Define dummy classes as fallback
        class DummyCrew:
            def kickoff(self, inputs):
                return "CrewAI not installed"
        Agent, Task, Crew, LLM = object, object, DummyCrew, lambda model, temperature: None

# Try to import SerperDevTool, with fallback
try:
    from crewai_tools import SerperDevTool
    serper_available = True
except ImportError:
    serper_available = False
    print("Warning: SerperDevTool not available")
    # Create dummy SerperDevTool
    class SerperDevTool:
        def __init__(self, api_key, **kwargs):
            self.api_key = api_key

class ResearchCrew:
    def __init__(self, topic, model="gemini/gemini-2.0-flash", temperature=0.7):
        self.topic = topic
        self.model = model
        self.temperature = temperature
        
        # Initialize LLM only if not in Streamlit Cloud
        if not is_streamlit_cloud():
            try:
                self.llm = LLM(model=self.model, temperature=self.temperature)
            except Exception as e:
                print(f"Error initializing CrewAI LLM: {e}")
                self.llm = None
        else:
            self.llm = None
            
    def setup_agents_and_tasks(self, serper_api_key=None):
        """Create and configure all necessary agents and tasks"""
        # For Streamlit Cloud, redirect to simplified approach immediately
        if is_streamlit_cloud():
            return None
            
        # Initialize search tool if API key is provided and tool is available
        search_tool = None
        if serper_api_key and serper_available:
            # Set the API key in the environment as well to ensure it's accessible
            os.environ["SERPER_API_KEY"] = serper_api_key
            
            # Create the search tool with more results and proper configuration
            try:
                search_tool = SerperDevTool(
                    api_key=serper_api_key,
                    n_results=5,  # Increase number of results
                    include_answer=True,
                    include_images=False,
                    include_related_searches=True
                )
            except Exception as e:
                print(f"Error initializing SerperDevTool: {e}")
                # Fallback to simple initialization if the extended parameters fail
                try:
                    search_tool = SerperDevTool(api_key=serper_api_key)
                except Exception:
                    search_tool = None
        
        # Create agents
        research_analyst = self._create_research_analyst(search_tool)
        content_writer = self._create_content_writer()
        
        # Create tasks
        research_task = self._create_research_task(research_analyst)
        writing_task = self._create_writing_task(content_writer)
        
        # Create crew
        try:
            crew = Crew(
                agents=[research_analyst, content_writer],
                tasks=[research_task, writing_task],
                verbose=True
            )
            return crew
        except Exception as e:
            print(f"Error creating crew: {e}")
            # If we can't create a proper crew, return a simple error message
            return None
            
    def _create_research_analyst(self, search_tool=None):
        """Create research analyst agent"""
        tools = [search_tool] if search_tool and search_tool is not None else []
        
        return Agent(
            role="Senior Research Analyst",
            goal=f"Research, analyze, and synthesize comprehensive information on {self.topic} from reliable web sources",
            backstory="You're an expert research analyst with advanced web research skills. "
                    "You excel at finding, analyzing, and synthesizing information from "
                    "across the internet using search tools. You're skilled at "
                    "distinguishing reliable sources from unreliable ones, "
                    "fact-checking, cross-referencing information, and "
                    "identifying key patterns and insights. You provide "
                    "well-organized research briefs with proper citations "
                    "and source verification. Your analysis includes both "
                    "raw data and interpreted insights, making complex "
                    "information accessible and actionable.",
            allow_delegation=False,
            verbose=True,
            tools=tools,
            llm=self.llm
        )
    
    def _create_content_writer(self):
        """Create content writer agent"""
        return Agent(
            role="Content Writer",
            goal="Transform research findings into engaging blog posts while maintaining accuracy",
            backstory="You're a skilled content writer specialized in creating "
                    "engaging, accessible content from technical research. "
                    "You work closely with the Senior Research Analyst and excel at maintaining the perfect "
                    "balance between informative and entertaining writing, "
                    "while ensuring all facts and citations from the research "
                    "are properly incorporated. You have a talent for making "
                    "complex topics approachable without oversimplifying them.",
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )
    
    def _create_research_task(self, research_analyst):
        """Create research task"""
        return Task(
            description=(f"""
                1. Conduct comprehensive research on {self.topic} including:
                    - Recent developments and news
                    - Key industry trends and innovations
                    - Expert opinions and analyses
                    - Statistical data and market insights
                2. Evaluate source credibility and fact-check all information
                3. Organize findings into a structured research brief
                4. Include all relevant citations and sources
            """),
            expected_output="""A detailed research report containing:
                - Executive summary of key findings
                - Comprehensive analysis of current trends and developments
                - List of verified facts and statistics
                - All citations and links to original sources
                - Clear categorization of main themes and patterns
                Please format with clear sections and bullet points for easy reference.""",
            agent=research_analyst
        )
    
    def _create_writing_task(self, content_writer):
        """Create writing task"""
        return Task(
            description=("""\
                Using the research brief provided, create an engaging blog post that:
                1. Transforms technical information into accessible content
                2. Maintains all factual accuracy and citations from the research
                3. Includes:
                    - Attention-grabbing introduction
                    - Well-structured body sections with clear headings
                    - Compelling conclusion
                4. Preserves all source citations in [Source: URL] format
                5. Includes a References section at the end
            """),
            expected_output="""A polished blog post in markdown format that:
                - Engages readers while maintaining accuracy
                - Contains properly structured sections
                - Includes Inline citations hyperlinked to the original source url
                - Presents information in an accessible yet informative way
                - Follows proper markdown formatting, use H1 for the title and H3 for the sub-sections""",
            agent=content_writer
        )
    
    def generate_content(self, serper_api_key=None):
        """Execute the crew to generate content"""
        # For Streamlit Cloud, use simplified generator instead
        if is_streamlit_cloud():
            try:
                from src.utils.simplified_generator import generate_simple_content
                # Get the API key from environment if not provided
                gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
                return generate_simple_content(self.topic, gemini_api_key)
            except Exception as e:
                return f"Error generating content: {str(e)}"
        
        # Regular approach for local environment
        try:
            crew = self.setup_agents_and_tasks(serper_api_key)
            if crew is None:
                return "Error: Could not initialize CrewAI. Please check your API keys and try again."
                
            result = crew.kickoff(inputs={"topic": self.topic})
            
            # Extract the string content from CrewOutput object
            if hasattr(result, 'raw'):
                return result.raw
            elif hasattr(result, 'result'):
                return result.result
            elif isinstance(result, str):
                return result
            else:
                # If we can't determine how to extract content, convert to string
                return str(result)
        except Exception as e:
            error_msg = str(e)
            print(f"Error generating content: {error_msg}")
            
            # Generate a fallback response if there's an error
            fallback = f"""
            # Research on {self.topic}
            
            I apologize, but I encountered an issue while trying to research this topic using external tools.
            
            Here's what I can tell you about {self.topic} based on my general knowledge:
            
            - {self.topic} is an important area of interest
            - To learn more about this topic, consider exploring recent academic journals, news sources, or expert opinions
            - For more detailed and up-to-date information, please try again or refine your topic
            
            Error details: {error_msg}
            """
            return fallback