import logging
import json
import re
from openai_config import call_openai_chat
from schemas import LiteratureOutput

def clean_json_string(raw: str) -> str:
    # Remove trailing commas and fix common formatting issues
    raw = re.sub(r",\s*}", "}", raw)
    raw = re.sub(r",\s*]", "]", raw)
    raw = raw.replace("'", '"')
    return raw.strip()

def literature_mining(query):
    logging.info("[LITERATURE_AGENT] Query: " + query)

    prompt = [
        {
            "role": "system",
            "content": "You are a biomedical literature expert. Always return a JSON object with fields: papers (list of {title, id}) and source_databases (list)."
        },
        {
            "role": "user",
            "content": f"""Search for recent studies on: "{query}". Return results in JSON only."""
        }
    ]

    try:
        response = call_openai_chat(prompt)
        raw = response.choices[0].message.content.strip()
        logging.info(f"[LITERATURE_AGENT] Raw OpenAI response:\n{raw}")

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            cleaned = clean_json_string(raw)
            parsed = json.loads(cleaned)

        validated = LiteratureOutput(**parsed)
        logging.info(f"[LITERATURE_AGENT] ✅ Parsed {len(validated.papers)} papers from {validated.source_databases}")
        return validated.dict()

    except Exception as e:
        logging.error(f"[LITERATURE_AGENT] ❌ Failed to parse OpenAI response: {e}")
        return {
            "papers": [],
            "source_databases": []
        }
