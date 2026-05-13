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


import os
import json
from openai import OpenAI


def generate_swot(idea, category):

    api_key = os.environ.get("api_key")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    prompt = f"""
    Generate a SWOT analysis for this business idea.

    Category: {category}
    Idea: {idea}

    Return JSON only with:
    strengths, weaknesses, opportunities, threats
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        data = json.loads(content)

        return {
            'strengths': data.get('strengths', []),
            'weaknesses': data.get('weaknesses', []),
            'opportunities': data.get('opportunities', []),
            'threats': data.get('threats', []),
        }

    except Exception as e:
        print("ERROR:", e)
        raise SWOTGenerationError(str(e))