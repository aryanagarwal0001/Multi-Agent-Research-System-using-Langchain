from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic : str) -> str:
    
    state = {}
    
    # search agent working
    print("\n"+" ="*50)
    print("Step 1 - search agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {
            "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}. "
            "You MUST format your final response EXACTLY like this for each result found:\n"
            "Title: [Insert Title]\nURL: [Insert URL]\nSnippet: [Insert Snippet]\n")]
        }
    )
    state["search_results"] = search_result["messages"][-1].content

    print("\n search result ", state["search_results"])

    # reader agent working

    print("\n" + "=" * 50)
    print("Step 2 - reader agent working...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" : [("user", 
                       f"Based on the following search results about '{topic}', "
                       f"pick the most relevant URL and scrape it for deeper content.\n\n"
                       f"Search Results: \n{state['search_results']}"
                       )]
    }) 

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nscraped content: \n", state["scraped_content"])
    
    # writer chain 

    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined =(
        f"SEARCH_RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']} \n"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report \n", state["report"])

    # Critic Chain

    print("\n" + "=" * 50)
    print("Step 4 - Critic is checking the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report" : state["report"]
    })

    print("\n Critic Report \n", state["feedback"])

    return state