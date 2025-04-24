from openai_config import client

def generate_final_report(literature, biomarkers, pathways):
    assistant = client.beta.assistants.create(
        name="Scientific Report Generator",
        instructions=(
            "You are a biomedical scientist. Generate a report using literature findings, biomarker "
            "stats, and pathway/drug insights. Use structured natural language and output sections: "
            "Introduction, Biomarker Analysis, Pathway Mapping, Drug Insights, Conclusion."
        ),
        model="gpt-4",
        tools=[],
        temperature=0.4,
        logit_bias={},
        response_format="auto"
    )

    thread = client.beta.threads.create()

    full_context = (
        f"LITERATURE:\n{literature}\n\n"
        f"BIOMARKERS:\n{biomarkers}\n\n"
        f"PATHWAYS:\n{pathways}"
    )

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=full_context
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        stream=True,
        tool_choice="auto",
        function_call="auto",
        max_tokens=800
    )

    from openai import Stream
    result = []
    for chunk in run:
        if hasattr(chunk, "delta") and hasattr(chunk.delta, "content"):
            result.append(chunk.delta.content)
    return ''.join(result).strip()
