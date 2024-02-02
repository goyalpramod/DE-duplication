import json
from app.retriever_search import retrieve_relevant_docs

# {"original_task_1_id" : ["duplicate_1_id","duplicate_2_id"]}
task_id = {
    "4e9b7ecd-60ae-4b35-ae8c-22393abcd119": ["d2f3g4h5-i6j7-k8l9-m1n2-o3p4q5r6s7t8"],
    "6a8dcef8-3dae-4567-ada4-1a2b3c4d5e6f": ["u7v8w9x0-y1z2-a3b4-c5d6-e7f8g9h0i1j2"],
    "8bd5fcea-3c56-4771-ac41-54321fe98734": ["k9l8m7n6-o5p4-q3r2-s1t0-u8v9w7x6y5z4", "fad3c2b1-a4e5-f6d7-89b0-c1d2e3f4b5a6"],
    "7b8e9d2c-69d1-48a7-b3f1-45678ef9abcd": ["v6b7n8m9-c5x4-z3a2-s1e9-d8f7g6h5i4j3"],
    "eaf7892b-b880-4b57-985c-2a3d4e5678f9": ["z0y9x8w7-v6u5-t4s3-r2q1-p0o9n8m7l6k5", "i8u7y6t5-r4e3-w2q1-a1s2-d3f4g5h6i7j8", "p0l9k8j7-h6g5-f4d3-s2a1-q1w2e3r4t5y6"],
    "9f8d7c6e-ab7d-4e2c-8c34-56789f0ed3f2": ["m4n5b6v7-c8x9-z0l1-k2j3-h4g5f6d7s8a9"],
    "cab4d5e6-f7a8-b9c0-de12-34f56g7h8i9j": ["z9x8c7v6-b5n4-m3l2-k1j8-h7g6f5d4s3a2"],
    "m9n8b7v6-c5x4-z3a2-s1d9-f8g7h6j5k4l3": ["q1w2e3r4-t5y6-u7i8-o9p0-a1s2d3f4g5h6"]
}

# Load the JSON data from the file
def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to match the ID and return its description
def get_description_for_id(_id, data):
    for item in data:
        if item['Id'] == _id:
            return item['description']
    return None  # Return None if ID not found

list_of_original_id = list(task_id.keys())

temp_docs = []

# Path to your JSON file
json_file_path = 'data/dummy.json'
# Load the data from JSON file
json_data = load_json_data(json_file_path)

temp_docs = []
for _id in list_of_original_id:
    # Get the description for the current ID
    description = get_description_for_id(_id, json_data)
    # Check if description was found
    if description:
        # Call the function with the description as a query, and append the result to temp_docs
        temp_docs.append(retrieve_relevant_docs(query=description))
    else:
        print(f"No description found for ID: {_id}")

# Define the file name
file_name = "temp_docs.txt"

# Open a file in write mode
with open(file_name, 'w', encoding='utf-8') as file:
    # Iterate through each list in temp_docs
    for doc_tuple_list in temp_docs:
        # Iterate through each tuple (Document, float) in the list
        for doc_tuple in doc_tuple_list:
            # Assuming doc_tuple[0] is the Document and has a to_string() method
            # Replace `doc_tuple[0].to_string()` with `document_to_string(doc_tuple[0])` if necessary
            doc_rep = doc_tuple[0].page_content
            doc_id = doc_tuple[0].metadata['Id']
            # Convert the float to string and prepare the entire tuple as a string
            tuple_str = f"({doc_rep}, {doc_tuple[1]}, {doc_id})"
            # Write the string representation of the tuple to the file
            file.write(tuple_str + '\n')
        file.write('\n')

print(f"Data saved to '{file_name}' successfully.")



