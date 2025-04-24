import random
from openai_config import client

def generate_bioinformatics_style_query():
    gene = random.choice([
        "TP53", "BRCA1", "BRCA2", "EGFR", "KRAS", "PIK3CA", "APC", "PTEN",
        "MLH1", "ATM", "CDKN2A", "NRAS", "BRAF", "VHL", "ALK", "NOTCH1",
        "IDH1", "FGFR3", "MET", "SMAD4"
    ])

    prompt = f"Provide information regarding {gene} gene, including its biomarker role, associated pathways, and drug targets."

    # ✅ Create Assistant
    assistant = client.beta.assistants.create(
        name="Scientific Query Generator",
        instructions="You are a biomedical assistant generating concise biomarker queries for further analysis.",
        model="gpt-4"
    )

    # ✅ Create a thread
    thread = client.beta.threads.create()

    # ✅ Add user message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    # ✅ Create the run — no model control arguments here!
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value.strip()
