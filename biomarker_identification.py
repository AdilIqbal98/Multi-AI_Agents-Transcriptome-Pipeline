from openai_config import client
from schemas import BiomarkerOutput
import pandas as pd
import json
import re
from utils import validate_and_retry

def run_biomarker_agent(count_file: str) -> BiomarkerOutput:
    df = pd.read_csv(count_file, index_col=0)
    summary = f"{df.shape[0]} genes × {df.shape[1]} samples"

    def _run(_):
        assistant = client.beta.assistants.create(
            name="Biomarker Agent",
            instructions=(
                "You are a transcriptomic analyst. Given sequencing data context, simulate realistic DESeq2-like output. "
                "Return only real, known human gene names—avoid placeholders like GENE_XYZ. "
                "Output valid JSON with fields: "
                "'known_biomarkers': list of dicts with 'gene', 'condition'; "
                "'novel_predictions': list of dicts with 'gene', 'condition'; "
                "'deg_results': list of dicts with 'gene', 'log2FoldChange', 'pvalue', 'padj'."
            ),
            model="gpt-4"
        )

        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Simulate biomarker output based on gene expression matrix summary: {summary}"
        )

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        raw = messages.data[0].content[0].text.value.strip()

        print("🧬 Raw Biomarker Output:\n", raw)

        try:
            json_str = re.search(r"\{.*\}", raw, re.DOTALL).group()
            parsed = json.loads(json_str)
            return BiomarkerOutput(**parsed)
        except Exception as e:
            print("❌ JSON parsing failed:", e)
            print("🔍 Raw GPT output:\n", raw)
            raise

    return validate_and_retry(_run, validator_func=None, input_data=None, agent_name="Biomarker Agent")
