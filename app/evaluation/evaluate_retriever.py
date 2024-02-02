from app.retriever_search import retrieve_relevant_docs
from typing import List, Tuple, Literal, Optional
import json

def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def evaluate_tasks(tasks: List[dict]) -> List[dict]:
    evaluation_results = []
    
    for task in tasks:
        relevant_docs = retrieve_relevant_docs(task["description"])
        task_result = {
            "Id": task["Id"],
            "Label": task["Label"],
            "Scores": [score for _, score in relevant_docs],
        }
        
        # if task["Label"] == 1:
        #     # Check if the ID of any returned document matches the task's "Duplicate of" value
        #     matches = any(doc.metadata.get("Id") == task["Duplicate of"] for doc, _ in relevant_docs)
        #     task_result["DuplicateMatch"] = matches
        if task["Label"] == 1:
            # Instead of checking any document, we check only the first document
            if relevant_docs:  # Ensuring there is at least one document
                first_doc = relevant_docs[0][0]  # Accessing the first document in the list of tuples
                matches = first_doc.metadata.get("Id") == task["Duplicate of"]
            else:
                matches = False  # If there are no relevant_docs, then it doesn't match
            task_result["DuplicateMatch"] = matches

        evaluation_results.append(task_result)
        
    return evaluation_results

if __name__ == "__main__":
    json_file_path = 'data/_test.json'
    json_data = load_json_data(json_file_path)
    evaluation_results = evaluate_tasks(json_data)
    print(evaluation_results)
    # Save the evaluation results to a text file
    with open("evaluation_results_for_1st_val.txt", "w") as file:
        for result in evaluation_results:
            file.write(json.dumps(result) + "\n")