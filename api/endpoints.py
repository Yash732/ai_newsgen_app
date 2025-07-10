from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.graph_builder import build_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

graph = build_graph()

class GraphInput(BaseModel):
    mode: str # update or query
    user_input: str = "" #Optional

@app.get("/")
async def greet():
    return {
        "response": "Hello user"
    }

@app.post("/run_graph")
async def run_graph(input:GraphInput):
    state = {
        "mode": input.mode
    }
    if input.mode == "query":
        state['user_input'] = input.user_input
    
    try: 
        output = await graph.ainvoke(state)
        return {
            "response": output.get("agent_response", "No response generated")

        }
    except Exception as e:
        return {
            "error": str(e)
        }