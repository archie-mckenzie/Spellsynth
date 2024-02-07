# Spellsynth

<i>Currently under construction. Please check back later.</i>

A System for Fine-Tuning <b>Spe</b>cialized <b>L</b>arge <b>L</b>anguage Models from <b>Synth</b>etic Data 

<a href='http://spellsynth.com'>spellsynth.com</a>

Archie McKenzie '24
<br/>
Department of Computer Science
<br/>
Princeton University

2023-24 Thesis
<br/>
Advised by Professor Brian Kernighan

## Introduction

Spellsynth is system for creating synthetic datasets to fine-tune powerful LLM translators.

In addition to code and instructions, this repo contains two Spellsynth fine-tuning datasets, each of about 20,000,000 tokens:

<ul>
    <li><code>spellsynth-el</code></li>
    <li><code>kaleidograph</code></li>
</ul>

The datasets in <code>data/final</code> are freely licensed. They are intended as fine-tuning data for state-of-the-art LLMs like Mistral's <code>mixtral-8x7b</code>, Meta's <code>llama</code> models, or OpenAI's <code>gpt-4</code>.

In the interests of reproducibility, this research has used only open weights models and publicly available data.

## Prerequisites

- Python >3.11.6 installed
- pip installed

## Setup

### Create a Virtual Environment
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root directory and add the following:

```bash
TOGETHER_API_KEY='[YOUR API KEY]'
```

You only need API keys for the platforms you are using. Any platform that can serve language models like <code>mixtral-8x7b-instruct</code> (or equivalent) and embedding models like <code>m2-bert-80M-2k-retrieval</code> (or equivalent) will likely work. I have used <a href='https://together.ai'>Together.ai</a>.

## Data

### Sourcing

### Specification

### Example
