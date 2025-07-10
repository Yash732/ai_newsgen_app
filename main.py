from graph.graph_builder import build_graph
import asyncio
graph = build_graph()
image = graph.get_graph().draw_mermaid_png()
with open("ai_newsgen_graph.png", "wb") as f:
    f.write(image)

async def test_graph():

    print("Graph built successfully!")
    # # Example query to test agent path
    response =await graph.ainvoke({
        "mode": "query",
        "user_input": "Latest news on tourism in Kashmir after Pahalgam attack. Use tools only. Do not answer directly.",
    })
    print("completion: ", response)
if __name__ == "__main__":
    asyncio.run(test_graph())

