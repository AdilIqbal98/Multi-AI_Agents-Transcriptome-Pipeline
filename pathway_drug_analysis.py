import logging
import json
from openai_config import call_openai_chat
from schemas import PathwayOutput

def pathway_drug_analysis(biomarkers):
    combined = biomarkers.get("known_biomarkers", []) + biomarkers.get("novel_predictions", [])

    prompt = [
        {
            "role": "system",
            "content": "Map biomarkers to pathways and drug targets. Return a JSON object with keys as gene names and values as {pathways: [...], drug_targets: [...]}."
        },
        {
            "role": "user",
            "content": f"""Genes: {combined}"""
        }
    ]

    try:
        response = call_openai_chat(prompt)
        raw = response.choices[0].message.content.strip()
        logging.info(f"[PATHWAY_AGENT] Raw output:\n{raw}")

        gene_map = json.loads(raw)

        # Flatten gene_map into list of pathways and list of drug_targets
        all_pathways = set()
        all_drugs = set()

        for gene, info in gene_map.items():
            all_pathways.update(info.get("pathways", []))
            all_drugs.update(info.get("drug_targets", []))

        result = PathwayOutput(
            pathways=sorted(list(all_pathways)),
            drug_targets=sorted(list(all_drugs))
        )
        return result.dict()

    except Exception as e:
        logging.error(f"[PATHWAY_AGENT] ❌ Failed to parse pathway response: {e}")
        return {
            "pathways": [],
            "drug_targets": []
        }
