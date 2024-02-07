# embed.py
# embeds a list of strings using Together Compute's API
# https://docs.together.ai/reference/embeddings

# ---- IMPORTS ----- #

import aiohttp
import asyncio

import os
from dotenv import load_dotenv

# ----- SETUP ----- #

load_dotenv()

url = "https://api.together.xyz/v1/embeddings"
model = "togethercomputer/m2-bert-80M-2k-retrieval"
authorization = f'Bearer {os.environ.get("TOGETHER_API_KEY")}'
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": authorization
}

# ----- FUNCTIONS ----- #

async def __embed(text: str, session):
    payload = {
        "model": model,
        "input": text
    }
    result = None
    try:
        async with session.post(url, json=payload, headers=headers) as response:
            result = await response.json()
            return result['data'][0]['embedding']
    except Exception as exception:
        print(exception)
        if (result): print(result)
        return None

async def __embed_array(array: list[str], max_concurrent: int):
    final = []
    so_far = 0
    async with aiohttp.ClientSession() as session:
        chunked_text = [array[i:i+max_concurrent] for i in range(0, len(array), max_concurrent)]
        for chunk in chunked_text:
            result = await asyncio.gather(*[__embed(text, session) for text in chunk])
            final.extend(result)
            so_far += len(chunk)
            print(so_far)
    return final

# embeds an array of strings
def embed(array: list[str], max_concurrent: int = 1):
    return asyncio.run(__embed_array(array, max_concurrent))