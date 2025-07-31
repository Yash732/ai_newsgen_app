from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.graph_builder import build_graph
import datetime
from ai_resources.initialize_db import download_text_from_bucket
import re
from typing import Optional
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

graph = build_graph()
image = graph.get_graph().draw_mermaid_png()
with open("ai_newsgen_graph.png", "wb") as f:
    f.write(image)
class GraphInput(BaseModel):
    mode: str # update or query
    user_input: str = "" #Optional
    genre: Optional[str] = None

def parse_articles_to_json(text: str):
    """
    Extract articles based strictly on numbered patterns (e.g., '1. ...', '2. ...').
    Splits on numbering and uses the first line as title, rest as news.
    """
    # Match all numbered articles using a regex with lookahead for strict separation
    matches = re.findall(r'\d+\.\s+(.*?)(?=\n\d+\.|\Z)', text.strip(), re.DOTALL)

    parsed = []
    for article in matches:
        lines = article.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        news = "\n".join(line.strip() for line in lines[1:]).strip()
        parsed.append({"title": title, "news": news})

    return parsed

@app.get("/")
async def greet():
    return {
        "response": "Hello user"
    }
@app.get("/")
def health_check():
    """
    A simple endpoint to confirm the server is running.
    """
    return {"status": "ok"}

@app.post("/run_graph")
async def run_graph(input:GraphInput):
   
    state = {
        "mode": input.mode,
    }
    if input.mode == "update":
        genre = input.genre or "finance"
        print(f"Entered UPDATE mode +++ with genre: {genre}")
        today = datetime.date.today().isoformat()
        file_name = f"{genre}_{today}.txt"
        try:
            summary = download_text_from_bucket("dailynews", file_name)
            print("Summary fetched +++", summary[:50])
            articles = parse_articles_to_json(summary)

            return {"response": articles}
        except Exception as e:
            return {"error": f"Could not fetch today's update: {str(e)}"}

    elif input.mode == "query":
        print("Entered QUERY mode +++")
        state['user_input'] = input.user_input
        try: 
            output = await graph.ainvoke(state)
            summary = output.get("summary", "No response from backend")
            print("Summary fetched +++", summary[:50])
            articles = parse_articles_to_json(summary)

            return {"response": articles}
        except Exception as e:
            return {
                "error": str(e)
            }
    else:
        return {"error": "Invalid mode. Use 'update' or 'query'."}
    
# if __name__ == "__main__":
#     articles = parse_articles_to_json(
#         f"1. Title: Major AI Industry Initiatives and Investments Announced for 2025\n"
# f"News: In May–July 2025, OpenAI, SoftBank, and Oracle announced a collaboration on \"The Stargate Project,\" an ambitious plan to invest up to $500 billion in AI infrastructure across the United States. OpenAI and SoftBank also plan to build a small data center by the end of 2025 to support the Stargate AI initiative. SoftBank is negotiating a major investment in OpenAI, with potential collaborations in robotics, AI infrastructure, and chip development via Arm. The deal could create synergies between SoftBank’s hardware holdings and OpenAI’s software leadership. (Sources: Industry reports, May–July 2025)"

# f"2. Title: Google Releases Gemini 2.0, Its Most Advanced AI Model\n"
# f"News: Google has announced the release of Gemini 2.0, its most capable AI model to date. The new model features advanced \"agentic\" capabilities, enabling developers, enterprises, and individuals to leverage autonomous AI systems that can act independently and make decisions with minimal human intervention. (Source: Google AI Blog, 2025)"

# f"3. Title: The Rise of Agentic AI: Autonomous Systems Take Center Stage\n"
# f"News: Recent developments in AI have seen the emergence of agentic or autonomous AI systems. These systems are capable of acting independently, making decisions, and performing complex tasks with little to no human oversight, marking a significant leap forward in AI technology. (2025)")
#     print(articles)