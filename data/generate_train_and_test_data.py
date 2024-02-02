import json

def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def distribute_tasks(data):
    train_data = []
    test_data = []
    
    original_tasks = [task for task in data if task["Label"] == 0]
    duplicate_original_tasks = [task for task in data if task["Label"] == 1 and not task["Duplicate of"]]
    duplicate_tasks = [task for task in data if task["Label"] == 1 and task["Duplicate of"]]
    
    # Since you mentioned there are 40 original and 20 pairs of duplicates, 
    # dividing original tasks equally into train and test
    half_original_tasks = len(original_tasks) // 2
    train_data.extend(original_tasks[:half_original_tasks])
    test_data.extend(original_tasks[half_original_tasks:])
    
    # Adding duplicate original tasks to train data
    train_data.extend(duplicate_original_tasks)
    # Adding duplicates to test data
    test_data.extend(duplicate_tasks)
    
    save_json_data('data/train.json', train_data)
    save_json_data('data/test.json', test_data)

# Your JSON file path
json_file_path = 'data\data_2.json'
json_data = load_json_data(json_file_path)

# Distribute the tasks into train.json and test.json
distribute_tasks(json_data)

print("Tasks distribution completed. Check 'train.json' and 'test.json' files.")