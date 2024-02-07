# complete.py
# https://docs.together.ai/reference/completions

# ---- IMPORTS ----- #

import aiohttp
import asyncio

import os
from dotenv import load_dotenv

import time, datetime

# ----- SETUP ----- #

load_dotenv()

url = "https://api.together.xyz/v1/completions"

model = "togethercomputer/llama-2-70b-chat" # "mistralai/Mixtral-8x7B-Instruct-v0.1"
model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
authorization = f'Bearer {os.environ.get("TOGETHER_API_KEY")}'
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": authorization
}

# ----- FUNCTIONS ----- #

async def __complete(prompt: str, session):
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 4096,
        "stop": ["</s>", "[/INST]"],
        "temperature": 0,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "n": 1,
        "stream": False
    }
    result = None
    try:
        async with session.post(url, json=payload, headers=headers) as response:
            result = await response.json()
            return result['choices'][0]['text'].strip()
    except Exception as exception:
        print(exception)
        if (result): print(result)
        return None

async def __complete_array(array: list[str], max_concurrent: int):
    final = []
    so_far = 0
    async with aiohttp.ClientSession() as session:
        chunked_text = [array[i:i+max_concurrent] for i in range(0, len(array), max_concurrent)]
        for chunk in chunked_text:
            result = await asyncio.gather(*[__complete(text, session) for text in chunk])
            final.extend(result)
            so_far += len(chunk)
            print(so_far)
    return final

# completes an array of strings
def complete(array: list[str], max_concurrent: int = 1):
    return asyncio.run(__complete_array(array, max_concurrent))