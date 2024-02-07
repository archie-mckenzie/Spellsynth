# format_final.py
# Formats synthesized datasets
# Author: Archie McKenzie
# script 3/3

# ----- IMPORTS ----- #

import json
import random
from tokens.count_tokens import count_tokens

# ----- HELPER FUNCTIONS ----- #

def __format_for_jsonl(prompt, completion):
    return json.dumps({"prompt": prompt, "completion": completion})

def __format_for_openai(prompt, completion):
    return json.dumps({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": completion}]})

def write_jsonl(json_strings, filepath):
    with open(filepath, 'w') as file:
        for json_string in json_strings:
            file.write(json_string + '\n')
    print("JSONL file written successfully.")

# ----- MAIN ----- #

def main(
        input_filepath: str, 
        output_filepath: str,
        openai_output_filepath: str, 
        max_tokens: int,
        max_labels_per_translation: int
    ):

    with open(input_filepath, 'r') as file:
        translations = json.load(file)

    total_token_count = 0

    i = len(translations) - 1

    jsonl_array = []
    openai_array = []
    
    while i >= 0 and total_token_count < max_tokens:
        
        content, completion = '', ''
        if (translations[i]["from"] == "en"):
            content = f"English:\n\n{translations[i]['en']}\n\nGreek:"
            completion = translations[i]['el']
        else:
            content = f"Greek:\n\n{translations[i]['el']}\n\nEnglish:"
            completion = translations[i]['en']
        
        prompt = ''
        if 'labels' in translations[i]:
            labels = translations[i]['labels']
            num_labels_to_add = random.randint(1, max_labels_per_translation)
            selected_labels = random.sample(labels, min(len(labels), num_labels_to_add))
            prompt = "Guidelines:\n\n"
            for label in selected_labels:
                prompt += f'{label}\n'
            prompt += '\n'
        
        prompt += content

        total_token_count += count_tokens(prompt)
        total_token_count += count_tokens(completion)

        jsonl_array.append(__format_for_jsonl(prompt, completion))
        openai_array.append(__format_for_openai(prompt, completion))

        i -= 1
    
    print(len(jsonl_array))
    write_jsonl(jsonl_array, output_filepath)
    write_jsonl(openai_array, openai_output_filepath)

if __name__ == '__main__':
    INPUT_FILEPATH = 'data/processed/from_processed/en-el.json'
    OUTPUT_FILEPATH = 'data/final/en-el.jsonl'
    OPENAI_OUTPUT_FILEPATH = 'data/final/openai-en-el.jsonl'
    MAX_TOKENS = 49000000
    MAX_LABELS_PER_TRANSLATION = 4
    main(
        INPUT_FILEPATH, 
        OUTPUT_FILEPATH,
        OPENAI_OUTPUT_FILEPATH, 
        MAX_TOKENS,
        MAX_LABELS_PER_TRANSLATION
    )