import json
import subprocess
import time

def run_mistral(text):
    try:
        result = subprocess.run(['ollama', 'run', 'mistral', text], capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Response timed out"
    except Exception as e:
        return f"Error: {e}"

def run_falcon(text):
    try:
        result = subprocess.run(['ollama', 'run', 'falcon', text], capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Response timed out"
    except Exception as e:
        return f"Error: {e}"

def run_llama2(text):
    try:
        result = subprocess.run(['ollama', 'run', 'llama2', text], capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Response timed out"
    except Exception as e:
        return f"Error: {e}"


def process_json_file(file_path):
    # Load JSON data from the file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    count = 1
    # Iterate over each question and generate a response using run_ollama
    for question_id, question_info in data.items():
        print("On question", count)
        title = question_info.get('title', '')
        responses = question_info.get('responses', [])
        combined_text = f"Following is a question posted on a forum, generate a helpful response that is less than 200 words: {title}"
        mistral_response = run_mistral(combined_text)
        falcon_response = run_falcon(combined_text)
        llama_response = run_llama2(combined_text)
        # Add the LLM response to the question info
        question_info['mistral_response'] = mistral_response
        question_info['faclon_response'] = falcon_response
        question_info['llama2_response'] = llama_response
        # Simulate delay to mimic the time taken for LLM response generation
        time.sleep(1)
        count+=1

    # Save the modified data back to the file (or to a new file if you prefer)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("JSON file has been updated with LLM responses.")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

# Replace 'your_json_file.json' with the actual path to your JSON file
process_json_file('organized_questions_with_responses')
