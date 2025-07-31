from graph.graph_builder import build_graph
from ai_resources.initialize_db import upload_text_to_bucket
import datetime
import asyncio

def run_update():
    
    today = datetime.date.today().isoformat()
    genres = ['finance', 'sports','technology', 'politics','gaming']
    # genres = ['finance', 'sports']
    async def process_genre(genre):
        graph = build_graph()
        state = {
            "mode": "update",
            "genre": genre
            }
        try:
            output = await graph.ainvoke(state)
            summary = output.get("summary", "No response generated")
            file_name = f"{genre}_{today}.txt"

            #save to supabase storage bucket
            upload_text_to_bucket("dailynews", file_name, summary)
        except Exception as e:
            print(f"Failed for {genre}: {e}")

    async def main():
        for genre in genres:
            await process_genre(genre)
            await asyncio.sleep(120)  # wait to respect Azure rate limits
    asyncio.run(main())
if __name__ == "__main__":
    run_update()


