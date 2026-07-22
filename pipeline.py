from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str):
    """
    Generator version of the pipeline.
    Yields status events as each agent runs, and finally yields the result.

    Event shapes:
      {"type": "status", "step": "search",  "state": "active", "message": "..."}
      {"type": "status", "step": "search",  "state": "done",   "message": "..."}
      {"type": "result", "data": {...}}
      {"type": "error",  "message": "..."}
    """
    state = {}

    try:
        # ---------------- Step 1: Search ----------------
        yield {"type": "status", "step": "search", "state": "active",
               "message": f"Searching the web for '{topic}'..."}

        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        search_messages = search_result.get("messages", [])
        state["search_results"] = search_messages[-1].content if search_messages else ""

        yield {"type": "status", "step": "search", "state": "done",
               "message": "Search complete."}

        # ---------------- Step 2: Read / Scrape ----------------
        yield {"type": "status", "step": "read", "state": "active",
               "message": "Reading top sources and extracting content..."}

        reader_agent = build_reader_agent()
        reader_results = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}' "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        reader_messages = reader_results.get("messages", [])
        state["scraped_content"] = reader_messages[-1].content if reader_messages else ""

        yield {"type": "status", "step": "read", "state": "done",
               "message": "Content extraction complete."}

        # ---------------- Step 3: Write ----------------
        yield {"type": "status", "step": "write", "state": "active",
               "message": "Drafting the research report..."}

        research_combined = (
            f"SEARCH RESULTS: \n {state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT: \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })

        yield {"type": "status", "step": "write", "state": "done",
               "message": "Report drafted."}

        # ---------------- Step 4: Critic ----------------
        yield {"type": "status", "step": "critic", "state": "active",
               "message": "Reviewing report quality..."}

        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        yield {"type": "status", "step": "critic", "state": "done",
               "message": "Review complete."}

        # ---------------- Final result ----------------
        yield {"type": "result", "data": state}

    except Exception as e:
        yield {"type": "error", "message": str(e)}


if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    for event in run_research_pipeline(topic):
        print(event)