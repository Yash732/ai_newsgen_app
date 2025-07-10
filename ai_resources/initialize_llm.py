import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from smolagents import ToolCallingAgent, ToolCollection, LiteLLMModel
from litellm import completion
load_dotenv()
endpoint = "https://21bcg-mcj1blj5-eastus2.cognitiveservices.azure.com/"
# Initialize the model using Azure OpenAI or LiteLLMModel

def initialize_model():
    return AzureChatOpenAI(
    deployment_name="gpt-4.1",
    model_name="gpt-4.1",
    temperature=0.0,
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=endpoint,
    api_version="2024-12-01-preview"
)

def chat_with_model(prompts: str | list[str]):
    #handling the prompts
    # client = initialize_model()
    # if isinstance(prompts,str):
    #     prompts = [prompts]

    # responses = []
    # for prompt in prompts:
    #     response = client.chat.completions.create(
    #         model = deployment,
    #         messages = [{
    #             "role" :"user",
    #             "content": prompt
    #         }]
    #     )
    #     responses.append(response.choices[0].message.content)
    # return responses

    # liteLLM model
    model = LiteLLMModel(
        model_id = "ollama/phi3"
    )
    print("Initializing model...")
    responses = []
    print("Reading prompts", prompts)

    response = completion(
            model="ollama/phi3",
            messages=[
                    {"role": "user", "content": prompts}
                    ],
            api_base="http://localhost:11434"
            )
    responses.append(response.choices[0].message.content)
    print("Model initialized and responses generated.")
    return responses

# #testing
# response = chat_with_model("Hi. Can you teach me operational AI in 3 lines?")
# print(response[0])