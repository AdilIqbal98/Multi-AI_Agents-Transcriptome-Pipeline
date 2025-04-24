from openai_config import client
from schemas import PathwayOutput
from utils import validate_and_retry
import json
import re

def run_pathway_agent(genes: list) -> PathwayOutput:
    def _run(input_genes):
        assistant = client.beta.assistants.create(
            name="Pathway & Drug Mapping Agent",
            instructions=(
                "You are a biomedical informatics expert. Given gene names, return a JSON object containing "
                "'pathways': list of pathway names (strings) and "
                "'drug_targets': list of drug names (strings) targeting the input genes. "
                "Use only real human biological pathways (e.g., KEGG, Reactome) and real FDA-approved or experimental drug names. "
                "Avoid using placeholder or dummy data like 'Unknown' or 'GENE_XYZ'."
            ),
            model="gpt-4"
        )

        gene_list = ", ".join(input_genes)
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Map these biomarkers to pathways and drugs: {gene_list}"
        )

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        raw = messages.data[0].content[0].text.value.strip()

        print("🧪 Raw Pathway Output:\n", raw)

        try:
            json_str = re.search(r"\{.*\}", raw, re.DOTALL).group()
            nested = json.loads(json_str)

            # Flatten into two unique lists
            pathways_set = set()
            drug_set = set()
            for gene_info in nested.values():
                pathways_set.update(gene_info.get("pathways", []))
                drug_set.update(gene_info.get("drug_targets", []))

            return PathwayOutput(pathways=list(pathways_set), drug_targets=list(drug_set))
        except Exception as e:
            print("❌ Failed to parse pathway response:", e)
            raise

    return validate_and_retry(_run, validator_func=None, input_data=genes, agent_name="Pathway Agent")
