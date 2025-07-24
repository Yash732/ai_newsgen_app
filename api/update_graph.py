from graph.graph_builder import build_graph
from ai_resources.initialize_db import upload_text_to_bucket
import datetime
import asyncio

def run_update():
    graph = build_graph()
    state = {"mode": "update"}
    try:
        output = asyncio.run(graph.ainvoke(state))  # If async: use asyncio.run(graph.ainvoke(state))
        summary = output.get("summary", "No response generated")
    except Exception as e:
        summary = f"Error during update: {str(e)}"
    # Save to Supabase bucket
    today = datetime.date.today().isoformat()
    file_name = f"{today}.txt"
    upload_text_to_bucket("dailynews", file_name, summary)

if __name__ == "__main__":
    run_update()