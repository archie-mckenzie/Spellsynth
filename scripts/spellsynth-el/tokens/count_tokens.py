# count_tokens.py
# counts tokens using OpenAI's tiktoken tokenzier

import tiktoken

def count_tokens(string: str):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(string))