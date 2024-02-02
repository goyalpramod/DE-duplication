import os
from dotenv import load_dotenv, find_dotenv
import json 
import os
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_together import Together
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
load_dotenv(find_dotenv())

CHAT_MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1
NUM_EXAMPLES = 500

OUTPUT_FILE_PATH = "generated_datasets/data_2.csv"  # Change the output file path to store it in the root directory

openai_api_key = os.environ["OPENAI_API_KEY"]

prompt_template = """
You will generate mock data for a task management system. The data should be in the form of a json with the following structure:
{json_structure}
generate a 80 examples, with 40 being original task without having any duplicates and a pair of 20 tasks being duplicates of each other. in the duplicate tasks, each task should have only one duplicate. It should not be an exact duplicate, the id should be different and the description should be worded differently.
Remember: Generate only a json with the structure described above, and nothing else. 
"""

examples = []

parser = JsonOutputParser()
parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())

chat_model = ChatOpenAI(model=CHAT_MODEL, temperature=1)

generation_prompt = ChatPromptTemplate.from_template(prompt_template)
chain = generation_prompt | chat_model | parser

tool_examples = chain.invoke({"json_structure": """
[{
        "Id": "4e9b7ecd-60ae-4b35-ae8c-22393abcd119",
        "title": "Implement New Feature",
        "description": "Develop the new search functionality using elastic search.",
        "assigned": "John Doe",
        "progress": "In Progress",
        “Label”: 1,
        “Duplicate of”: “id_of_the_original_task”
    },
{
        "Id": "6a8dcef8-3dae-4567-ada4-1a2b3c4d5e6f",
        "title": "Bug Fix on Homepage",
        "description": "Address the layout breaking issue in the homepage when viewed on mobile devices.",
        "assigned": "Emily Clark",
        "progress": "Completed",
        “Label”: 0,
        “Duplicate of”: “”
    }]
"""})

examples.append(tool_examples)

df = pd.DataFrame(examples)

# Create the folder if it does not exist
folder_path = os.path.dirname(OUTPUT_FILE_PATH)
os.makedirs(folder_path, exist_ok=True)

df.to_csv(OUTPUT_FILE_PATH, index=False)
print("Dataset saved to:", OUTPUT_FILE_PATH)
print(df.head(20))
