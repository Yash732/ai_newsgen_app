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

# Uploading and downloading news text from the bucket for daily news
def upload_text_to_bucket(bucket: str, file_name: str, text: str):
    data = text.encode("utf-8")
    res = supabase.storage.from_(bucket).upload(file_name, data, {"content-type": "text/plain", "upsert": "true"})
    return res

def download_text_from_bucket(bucket: str, file_name: str):
    res = supabase.storage.from_(bucket).download(file_name)
    if hasattr(res, "decode"):
        return res.decode("utf-8")
    return res

if __name__ == "__main__":
    import datetime
    today = datetime.date.today().isoformat()
    text = "1. **PayPal launches cross-border payment platform with global wallet partnerships** PayPal announced the launch of PayPal World, a new global payments platform set to go live later in 2024. The platform will connect major payment systems and digital wallets, including PayPal, Venmo, NPCI International Payments (UPI), Mercado Pago, and Tenpay Global, collectively representing nearly two billion users. PayPal World will allow consumers to use their domestic wallets for international transactions, pay in local currency, and simplify cross-border money transfers. Businesses can access users from partner wallets without extra development, expanding their reach. PayPal and Venmo will become interoperable, enabling global money transfers between the two. In 2026, Venmo users will be able to shop at PayPal-accepting merchants. The platform will use open commerce APIs, support dynamic payment buttons, and is designed to be secure and technology-agnostic.\n 2. **Eternal soars, Deepinder Goyal adds ₹2,000 crore in 2 days as Blinkit overtakes food delivery** Eternal's shares surged over 21% in two days, reaching an all-time high of ₹311.60 on the NSE, driven by rapid growth in its quick commerce arm, Blinkit. Founder and CEO Deepinder Goyal's net worth increased by approximately ₹2,000 crore to ₹11,515 crore, with Forbes estimating his net worth at $1.9 billion. Eternal's market capitalization crossed ₹3 lakh crore, surpassing companies like Wipro and Tata Motors. Blinkit has overtaken Zomato in net order value, prompting brokerages like Jefferies, Goldman Sachs, and CLSA to raise target prices for Eternal, with Jefferies setting a target of ₹400. The rally also boosted shares of rival Swiggy and stakeholder Info Edge."
    file_name = f"{today}.txt"
    upload_text_to_bucket("dailynews", file_name, text)
    result = download_text_from_bucket("dailynews", file_name)
    print(result)
