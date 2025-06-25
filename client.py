from smolagents import ToolCallingAgent, ToolCollection, LiteLLMModel
from litellm import completion
from mcp import StdioServerParameters

model = LiteLLMModel(
    model_id = "ollama/phi3"
)


#for stdio
# server_params = StdioServerParameters(
#     command = "python",
#     args = ["server.py"],
#     env = None,
# )

# with ToolCollection.from_mcp(server_params, trust_remote_code = True) as tool_collection:
#     agent = ToolCallingAgent(tools = [*tool_collection.tools], model = model)
#     agent.run("stock price of IBM?")


#for sse
with ToolCollection.from_mcp({"url": "http://localhost:8000/mcp", "transport": "streamable-http"}, trust_remote_code = True) as tool_collection:
    agent = ToolCallingAgent(tools = [*tool_collection.tools], model = model)
    agent.run("stock price of IBM?")

#Querying the model

# response = completion(
#             model="ollama/phi3",
#             messages = [{ "content": "Hello, how are you?","role": "user"}],
#             api_base="http://localhost:11434"
# )

# print(response)