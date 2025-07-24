from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.graph_builder import build_graph
import datetime
from ai_resources.initialize_db import download_text_from_bucket
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

@app.get("/")
async def greet():
    return {
        "response": "Hello user"
    }

# @app.post("/run_graph")
# async def run_graph(input:GraphInput):
#     state = {
#         "mode": input.mode
#     }
#     if input.mode == "query":
#         state['user_input'] = input.user_input
    
#     try: 
#         output = await graph.ainvoke(state)
#         return {
#             "response": output.get("summary", "No response generated")

#         }
#     except Exception as e:
#         return {
#             "error": str(e)
#         }

@app.post("/run_graph")
async def run_graph(input:GraphInput):
   
    state = {
        "mode": input.mode
    }
    if input.mode == "update":
        today = datetime.date.today().isoformat()
        file_name = f"{today}.txt"
        try:
            summary = download_text_from_bucket("dailynews", file_name)
            return {"response": summary}
        except Exception as e:
            return {"error": f"Could not fetch today's update: {str(e)}"}

    elif input.mode == "query":
        state['user_input'] = input.user_input
        try: 
            output = await graph.ainvoke(state)
            return {
                "response": output.get("summary", "No response generated")

            }
        except Exception as e:
            return {
                "error": str(e)
            }
    else:
        return {"error": "Invalid mode. Use 'update' or 'query'."}