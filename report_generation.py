import logging
from openai_config import call_openai_chat

def generate_report(literature, biomarkers, analysis):
    logging.info("[REPORT_GENERATOR] Generating report...")

    prompt = [
        {
            "role": "system",
            "content": "You are an expert biomedical assistant generating structured reports."
        },
        {
            "role": "user",
            "content": f"""
Create a scientific report summarizing the following:

Literature Findings:
{literature}

Biomarker Analysis:
{biomarkers}

Pathway and Drug Mapping:
{analysis}

Include an integrated conclusion for translational research.
"""
        }
    ]

    response = call_openai_chat(prompt, stream=True)

    full_report = ""
    for chunk in response:
        content = getattr(chunk.choices[0].delta, "content", "")
        if content:
            print(content, end="", flush=True)
            full_report += content

    logging.info("[REPORT_GENERATOR] ✅ Report assembled.")
    return full_report
