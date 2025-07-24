from langgraph.graph import StateGraph
from langgraph.constants import START, END 
from graph.state import State
from graph.nodes import greet_node, news_scraper, summarize_articles, display_summary, save_embeddings, handle_user_query
import uuid

def build_graph():
    builder = StateGraph(State)

    # Nodes
    builder.add_node("greet", greet_node)
    builder.add_node("news_scraper", news_scraper)
    builder.add_node("save_embeddings", save_embeddings)
    builder.add_node("summarize_articles", summarize_articles)
    builder.add_node("display_summary", display_summary)
    builder.add_node("tool_handler", handle_user_query)

    # Edges

    builder.set_entry_point("greet")
    builder.add_conditional_edges(
        "greet",
        lambda s: s["mode"],
        {
            "update": "news_scraper",
            "query": "tool_handler"
        }
    )
    # Update flow
    builder.add_edge("news_scraper", "summarize_articles")
    builder.add_edge("news_scraper", "save_embeddings")
    builder.add_edge("summarize_articles", "display_summary")
    # builder.add_edge("display_summary", "save_embeddings")
    builder.add_edge("save_embeddings", END)

    builder.add_edge("display_summary", END)

    # User query flow (chat interface)
    builder.add_edge("tool_handler", "summarize_articles")

    return builder.compile()




