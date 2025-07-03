import os
from dotenv import load_dotenv
from openai import AzureOpenAI
load_dotenv()
endpoint = "https://21bcg-mcj1blj5-eastus2.cognitiveservices.azure.com/"
model_name = "o3-mini"
deployment = "o3-mini"

def initialize_model():
    #model initialization

    api_version = "2024-12-01-preview"
    return AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key= os.getenv("OPENAI_API_KEY"),
    )

def chat_with_model(prompts: str | list[str]):
    #model initialization
    # endpoint = "https://21bcg-mcj1blj5-eastus2.cognitiveservices.azure.com/"
    # model_name = "o3-mini"
    # deployment = "o3-mini"

    # api_version = "2024-12-01-preview"

    # client = AzureOpenAI(
    #     api_version=api_version,
    #     azure_endpoint=endpoint,
    #     api_key= os.getenv("OPENAI_API_KEY"),
    # )
    #handling the prompts
    client = initialize_model()
    if isinstance(prompts,str):
        prompts = [prompts]

    responses = []
    for prompt in prompts:
        response = client.chat.completions.create(
            model = deployment,
            messages = [{
                "role" :"user",
                "content": prompt
            }]
        )
        responses.append(response.choices[0].message.content)
    return responses

# #testing
# response = chat_with_model("Hi. Can you teach me operational AI in 3 lines?")
# print(response[0])