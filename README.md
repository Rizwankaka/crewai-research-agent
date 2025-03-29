# 🤖 AI Research & Content Writer

[![GitHub stars](https://img.shields.io/github/stars/Rizwankaka/crewai-research-agent?style=social)](https://github.com/Rizwankaka/crewai-research-agent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Rizwankaka/crewai-research-agent?style=social)](https://github.com/Rizwankaka/crewai-research-agent/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Rizwankaka/crewai-research-agent)](https://github.com/Rizwankaka/crewai-research-agent/issues)
[![GitHub license](https://img.shields.io/github/license/Rizwankaka/crewai-research-agent)](https://github.com/Rizwankaka/crewai-research-agent/blob/main/LICENSE)

<p align="center">
  <img src="https://img.freepik.com/free-vector/artificial-intelligence-concept-circuit-board-background-with-robot-arm_1017-41025.jpg" alt="AI Research Banner" width="600">
</p>

## 📚 Overview

This application leverages the power of **CrewAI** and **Large Language Models** to automatically research any topic and generate well-structured, factually accurate blog posts with proper citations. It creates a crew of AI agents that work together to:

1. 🔍 **Research Agent**: Searches the web for the latest and most relevant information
2. ✍️ **Content Writer**: Transforms technical information into engaging, readable content

## ✨ Features

- 🌐 **Web Research**: Utilizes Serper API to gather real-time information from across the web
- 📊 **Factual Accuracy**: Maintains factual integrity with proper citations and source references
- 📝 **Content Generation**: Creates well-structured, engaging blog posts in markdown format
- 🎨 **User-Friendly Interface**: Easy-to-use Streamlit web application with attractive design
- ⚙️ **Customizable Settings**: Adjust parameters like temperature to control creativity level
- 💾 **Downloadable Content**: Save your generated content as markdown files

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Gemini API Key ([Get one here](https://ai.google.dev/))
- Serper API Key ([Get one here](https://serper.dev/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Rizwankaka/crewai-research-agent.git
cd crewai-research-agent
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Usage

1. Enter your Gemini and Serper API keys in the sidebar
2. Type your desired content topic or question
3. Adjust any advanced settings if needed
4. Click "Generate Content" and wait for the AI to research and write
5. Download your generated content as a markdown file

## 🧩 How It Works

<p align="center">
  <img src="https://mermaid.ink/img/pako:eNptkU9PwzAMxb_KyblMGmxwCweQQAxpSKAJbhsvdZeINmldp0iV-u24XScQ4pbf8_Ozn71HVUeJSjVXYLwe8MycQ_BaGk1svUfHqVkMNzBJI8YcEoGlTJhuPM90C3ndQGFg4NDDmp0mC840r9qGmWc5A0vWV3CbLJma5XxuQWAH41I2neBrTLU-PhCyzpYQQnJyjIU1eYphOGGJr68koeUUFo9L6Iy3lKl_1FWk1PW_bJ5ZwlOPTrQOy5R-Kj8KcEakN6Z2JZiHe-Mbp5MYNw5jZ9t49Y2zmOU0fCEPTVXboKO6hlGw2xRCWrOKSrVOGhhVYrvLZm80gXaoNEXZ6_bLPeI7Kn2XSr9F-9vdD6dwge4?type=png" width="600">
</p>

The application follows this workflow:
1. User inputs a topic for research
2. Research Agent searches the web and compiles information
3. Content Writer transforms the research into readable content
4. The final article is presented to the user with citations

## 🛠️ Project Structure

```
crewai-researchagent/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
└── src/
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── research_crew.py # CrewAI agent definitions
    ├── ui/
    │   ├── __init__.py
    │   └── components.py    # UI components
    └── utils/
        ├── __init__.py
        └── config.py        # Configuration utilities
```

## 📈 Future Improvements

- [ ] Add more specialized research agents for different topics
- [ ] Implement memory to improve research quality over time
- [ ] Add support for more output formats (PDF, HTML, etc.)
- [ ] Integrate with more data sources beyond web search
- [ ] Implement real-time collaboration features

## 👨‍💻 Author

**Rizwan Rizwan**

[![GitHub](https://img.shields.io/badge/GitHub-Rizwankaka-black?style=flat&logo=github)](https://github.com/Rizwankaka)
[![Kaggle](https://img.shields.io/badge/Kaggle-rizwanrizwannazir-blue?style=flat&logo=kaggle)](https://www.kaggle.com/rizwanrizwannazir)
[![Facebook](https://img.shields.io/badge/Facebook-RIZWANNAZEEER-blue?style=flat&logo=facebook)](https://www.facebook.com/RIZWANNAZEEER)
[![Email](https://img.shields.io/badge/Email-researcher%40datafyassociates.com-red?style=flat&logo=mail.ru)](mailto:researcher@datafyassociates.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.io/) for the agent framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Serper](https://serper.dev/) for the search API
- [Google Gemini](https://ai.google.dev/) for the LLM capabilities