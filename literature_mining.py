from openai_config import client
from schemas import LiteratureOutput
from utils import validate_and_retry
import json, re

def run_literature_agent(query: str) -> LiteratureOutput:
    def _run(prompt):
        assistant = client.beta.assistants.create(
            name="Literature Agent",
            instructions="Simulate a biomedical literature search. Return a JSON with papers [{title, id}] and source_databases [].",
            model="gpt-4",
        )
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=f"Query: {prompt}")
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        raw = messages.data[0].content[0].text.value
        json_block = re.search(r"\{.*\}", raw, re.DOTALL)
        return LiteratureOutput(**json.loads(json_block.group()))
    
    return validate_and_retry(_run, validator_func=None, input_data=query, agent_name="Literature Agent")
