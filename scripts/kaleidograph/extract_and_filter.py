# extract_pairs.py
# extracts sentence pairs from WikiMatrix in JSON format
# Author: Archie McKenzie
# script 1/3

# ----- IMPORTS ----- #

from xml.etree import ElementTree as ET
from tokens.count_tokens import count_tokens
import json 
import string
from typing import List

# ----- FUNCTIONS ----- #

def __count_total_tokens(translations: List[dict]):
    total_words = sum(count_tokens(sentence["en"]) + count_tokens(sentence["el"]) for sentence in translations)
    return total_words

# simple heuristic to filter out bad sentences
def __is_too_much_punctuation(s: str):
    fraction_threshold = 0.2
    punct_count = sum(c in string.punctuation for c in s)
    if punct_count >= fraction_threshold * len(s):
        return True
    else:
        return False

def __filter_object(json_obj: dict) :
    if not (json_obj["en"] and json_obj["el"]):
        return False
    if __is_too_much_punctuation(json_obj["en"]) or __is_too_much_punctuation(json_obj["el"]):
        return False
    upper_threshold = 500
    lower_threshold = 10
    token_count = count_tokens(json_obj["en"])
    if token_count > upper_threshold or token_count < lower_threshold:
        print(f'filtered out text with token count {token_count}')
        return False
    return True

def __extract_parallel_sentences_from_tmx_file(tmx_file_path: str):
    tree = ET.parse(tmx_file_path)
    root = tree.getroot()
    translations = []
    for tu in root.findall('.//tu'):
        json_obj = {"en": "", "el": ""}
        for tuv in tu.findall('.//tuv'):
            lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang')
            text = tuv.find('.//seg').text
            if lang == "en" and text:
                json_obj["en"] = text
            elif lang == "el" and text:
                json_obj["el"] = text
        if __filter_object(json_obj):
            translations.append(json_obj)
    return translations

# ----- MAIN ----- #

def main(tmx_filepath: str, output_filepath: str):
    translations = __extract_parallel_sentences_from_tmx_file(tmx_filepath)
    print(__count_total_tokens(translations))
    with open(output_filepath, 'w') as file:
        json.dump(translations, file)

if __name__ == '__main__':
    TMX_FILEPATH = "data/raw/el-en.tmx"
    OUTPUT_FILEPATH = "data/processed/from_raw/wikimatrix-en-el.json"
    main(TMX_FILEPATH, OUTPUT_FILEPATH)