import logging
import json
import pandas as pd
from openai_config import call_openai_chat
from schemas import BiomarkerOutput

def identify_biomarkers(sequencing_data):
    logging.info(f"[BIOMARKER_AGENT] Loading: {sequencing_data}")
    try:
        df = pd.read_csv(sequencing_data, index_col=0)
        summary = f"Data has {df.shape[0]} genes across {df.shape[1]} samples."
    except Exception as e:
        logging.error(f"[BIOMARKER_AGENT] Error reading: {e}")
        return {"known_biomarkers": [], "novel_predictions": [], "deg_results": None}

    prompt = [
        {"role": "system", "content": "You're a genomics agent. Return JSON output only."},
        {"role": "user", "content": f"""Simulate DESeq2 results for: {summary}. 
Return JSON with:
- known_biomarkers: [str], 
- novel_predictions: [str], 
- deg_results: [{{
    gene, log2FoldChange, pvalue, padj
}}]"""}
    ]

    try:
        response = call_openai_chat(prompt)
        raw = response.choices[0].message.content.strip()
        logging.info(f"[BIOMARKER_AGENT] Raw OpenAI output:\n{raw}")
        parsed = json.loads(raw)
        validated = BiomarkerOutput(**parsed)
        return validated.dict()
    except Exception as e:
        logging.error(f"[BIOMARKER_AGENT] OpenAI parsing error: {e}")
        return {"known_biomarkers": [], "novel_predictions": [], "deg_results": None}
