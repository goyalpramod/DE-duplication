from langchain.callbacks import get_openai_callback
from app.chain import chain

with get_openai_callback() as cb:
    response = chain.invoke(
        "are there any tasks which are Perform UAT"
    )
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")