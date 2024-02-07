# synthesize.py
# Labels fine-tuning data using Mixtral-8x7B
# Author: Archie McKenzie
# script 2/3

# ----- IMPORTS ----- #

import json
import random
from tokens.count_tokens import count_tokens
from completions.complete import complete

# ----- MAIN ----- #

def main(
        input_filepath: str, 
        output_filepath: str, 
        en_to_el_prompt: str,
        el_to_en_prompt: str,
        num_of_labelled: int
    ):

    def __create_prompt(translation):
        prompt = '[INST]'
        if (translation["from"] == "en"):
            prompt += f'{translation["en"]}\n\n${translation["el"]}\n\n'
            prompt += f'{en_to_el_prompt}'
        else:
            prompt += f'{translation["el"]}\n\n${translation["en"]}\n\n'
            prompt += f'{el_to_en_prompt}'
        prompt += '[/INST]'
        return prompt

    with open(input_filepath, 'r') as file:
        translations = json.load(file)

    translations_with_metadata = [
        {
            "en": translation["en"],
            "el": translation["el"],
            "token_count": count_tokens(translation["en"]),
            "from": random.choice(["en", "el"])
        }
        for translation in translations
    ]

    sorted_translations = sorted(translations_with_metadata, key=lambda x: x['token_count'])
    
    labelling_start_index = (len(sorted_translations) - num_of_labelled)
    translations_to_be_labelled = sorted_translations[labelling_start_index:]
    
    prompts = [__create_prompt(translation) for translation in translations_to_be_labelled]

    print(len(prompts))

    completions = complete(prompts, 100)

    final_en_el = []
    synthesis_successes = 0
    synthesis_failures = 0
    for i, translation in enumerate(sorted_translations):
        if i < labelling_start_index:
            final_en_el.append({
                'en': translation['en'],
                'el': translation['el'],
                'from': translation['from']
            })
        else: 
            completion = None
            try:
                completion = completions[i - labelling_start_index]
                json_start = completion.find('{')
                json_end = completion.find('}')
                json_all = completion[json_start:json_end+1]
                json_completion = json.loads(json_all)
                final_en_el.append({
                    'en': translation['en'],
                    'el': translation['el'],
                    'from': translation['from'],
                    'labels': json_completion['labels']
                })
                synthesis_successes += 1
            except:
                print(completion)
                print('could not parse!')
                final_en_el.append({
                    'en': translation['en'],
                    'el': translation['el'],
                    'from': translation['from']
                })
                synthesis_failures += 1
        if (i >= labelling_start_index and i % 100):
            print(f'Completed {i + 1} / {len(sorted_translations)}')
            print(f'{synthesis_successes} / {len(completions)} synthesis successes')
            print(f'{synthesis_failures} / {len(completions)} synthesis failures')

    with open(output_filepath, 'w') as file:
        json.dump(final_en_el, file)
    
if __name__ == '__main__':
    INPUT_FILEPATH = 'data/processed/from_raw/wikimatrix-en-el.json'
    OUTPUT_FILEPATH = 'data/processed/from_processed/en-el.json'
    EN_TO_EL_PROMPT = 'Give an array with a few labels about the above translation from English to Modern Greek. Each label should be one sentence, phrased as an imperative, about important style, tone, or vocabulary of how the translation was done. (NOT THE CONTENT) Your array should be presented in JSON format: {"labels": [] // list of strings }.'
    EL_TO_EN_PROMPT = 'Give an array with a few labels about the above translation from Modern Greek to English. Each label should be one sentence, phrased as an imperative, about important style, tone, or vocabulary of how the translation was done. (NOT THE CONTENT) Your array should be presented in JSON format: {"labels": [] // list of strings }.'
    NUM_OF_LABELLED = 41200 # because there's an error rate of about 3%
    main(
        INPUT_FILEPATH, 
        OUTPUT_FILEPATH, 
        EN_TO_EL_PROMPT,
        EL_TO_EN_PROMPT,
        NUM_OF_LABELLED
    )