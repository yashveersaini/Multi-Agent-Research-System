# 🚀 MultiAgentIQ -- AI-Based Multi-Agent Research System

## 📌 Brief One Line Summary

An AI-powered multi-agent system that performs intelligent web research,
extracts structured insights, and automates information gathering using
LLM-driven agents and tools.

------------------------------------------------------------------------

## 📖 Overview

MultiAgentIQ is a full-fledged AI research system built using a
multi-agent architecture. It leverages Large Language Models (LLMs),
tool-based reasoning, and LCEL (LangChain Expression Language) pipelines
to perform deep web research and data extraction.

The system consists of specialized agents that collaborate with tools
like Tavily (for intelligent search) and BeautifulSoup (for web
scraping), orchestrated through a central React-style agent. This
enables automated, scalable, and context-aware research workflows.

------------------------------------------------------------------------

## ❗ Problem Statement

Traditional search systems provide raw links but lack structured
insights and automation. Manual research is time-consuming and
inefficient.

This project solves: - Inefficient manual web research\
- Lack of structured and summarized insights\
- Difficulty in extracting relevant data from multiple sources\
- No coordination between search and data extraction

------------------------------------------------------------------------

## 🧠 System Architecture

### 🔹 Multi-Agent Design

-   **Research Agent**
    -   Uses Tavily API for intelligent search\
    -   Retrieves relevant URLs and summaries
-   **Scraper Agent**
    -   Uses BeautifulSoup for web scraping\
    -   Extracts clean and structured content
-   **Controller (React Agent)**
    -   Coordinates between agents\
    -   Decides which tool/agent to use\
    -   Handles reasoning and workflow execution
-   **LCEL Pipeline (Runnables)**
    -   Chains agents and tools efficiently\
    -   Enables modular and scalable execution

------------------------------------------------------------------------

## 🛠 Tools and Technologies

-   **Backend:** Python\
-   **LLM / AI:** LangChain, Gemini API (Google GenAI)\
-   **Agents:** React Agent (LangChain)\
-   **Search Tool:** Tavily API\
-   **Web Scraping:** BeautifulSoup, Requests\
-   **Pipeline:** LCEL (LangChain Runnables)\
-   **Environment Management:** python-dotenv\
-   **Async / Networking:** httpx, aiohttp\
-   **Debugging:** Rich

------------------------------------------------------------------------

## ⚙️ Methods

-   Multi-agent orchestration using LangChain\
-   Tool-based reasoning with Tavily and BeautifulSoup\
-   Web search using Tavily API (semantic search)\
-   HTML parsing and content extraction using BeautifulSoup\
-   LCEL pipelines for chaining agents and tools\
-   Prompt-driven reasoning using Gemini LLM\
-   Modular tool design using `@tool` decorator

------------------------------------------------------------------------

## 💡 Key Insights

-   Separates **search and extraction responsibilities** using agents\
-   Enables **autonomous research workflows**\
-   Produces **structured and summarized outputs instead of raw links**\
-   Highly **scalable and modular architecture**\
-   Demonstrates real-world **agent collaboration**

------------------------------------------------------------------------

## 📊 Output / Workflow

-   **User Query Input**\
-   **Research Agent Execution**\
-   **Scraper Agent Execution**\
-   **Final AI Response**

------------------------------------------------------------------------

## ▶️ How to Run this Project on Local System?

### 1. Clone the repository

``` bash
git clone https://github.com/your-username/multi-agent-research-system.git
cd multi-agent-research-system
```

### 2. Create virtual environment

``` bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

    GOOGLE_API_KEY=your_gemini_api_key
    TAVILY_API_KEY=your_tavily_api_key

### 5. Run the application

``` bash
python main.py
```

------------------------------------------------------------------------

## 📈 Results & Conclusion

-   Built a multi-agent research pipeline\
-   Automated search + scraping + summarization\
-   Improved efficiency of information retrieval

------------------------------------------------------------------------

## 🔮 Future Work

-   Add memory systems\
-   Implement vector databases (RAG)\
-   Build frontend UI\
-   Deploy to cloud

------------------------------------------------------------------------

## ⭐ Final Note

This project demonstrates a production-level multi-agent AI system using
modern LLM engineering practices.
