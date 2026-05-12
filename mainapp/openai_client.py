import json
import os
from pathlib import Path
from openai import OpenAI


class SWOTGenerationError(Exception):
    pass


def _load_local_env():
    env_path = Path(__file__).resolve().parent.parent / '.env'

    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())


def generate_swot(idea, category):
    _load_local_env()

    api_key = 
    model =
    

    prompt = f"""
    Generate a unique SWOT analysis for this business idea.

    Category: {category}
    Idea: {idea}

    Return only JSON with:
    strengths, weaknesses, opportunities, threats"""

    client = OpenAI(api_key=)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': 'Return only valid JSON.'},
            {'role': 'user', 'content': prompt},
        ],
        response_format={'type': 'json_object'},
    )
    print(response)
    # OpenAI with response_format=json_object returns JSON in the message content.
    content = response.choices[0].message.content
    data = json.loads(content)


    return {
        'strengths': data['strengths'],
        'weaknesses': data['weaknesses'],
        'opportunities': data['opportunities'],
        'threats': data['threats'],
    }
