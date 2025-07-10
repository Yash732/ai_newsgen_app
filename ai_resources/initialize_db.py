import numpy as np 
import os
from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Union
load_dotenv()
#defining the embedding model
embed_key = os.getenv("EMBED_KEY")
endpoint = "https://yash-mcp-ai.cognitiveservices.azure.com/"
model_name = "text-embedding-3-small"
deployment = "text-embedding-3-small"

api_version = "2024-02-01"
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    api_key = embed_key,
    azure_endpoint= endpoint,
)
# Function to get embeddings for a list of strings
def get_embeddings(news_list: List[str])->List[List[float]]:
    response = client.embeddings.create(
    input= news_list,
    model=deployment
    )

    return [d.embedding for d in response.data]

#defining the database 
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Function to insert content and embeddings into Supabase
def insert_embeddings(news_list: List[str]):
    embeddings = get_embeddings(news_list)
    rows = []
    for content, embedding in zip(news_list, embeddings):
        rows.append({
            "content": content,
            "embedding": embedding
        })
    response = supabase.table("news_list").insert(rows).execute()
    return response

