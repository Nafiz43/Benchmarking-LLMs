import pandas as pd
import json

# Step 1: Read the JSON file
with open('organized_questions_with_responses', 'r') as file:
    data = json.load(file)

# Step 2: Parse the JSON data
# Assuming 'data' is a dictionary that contains multiple entries like the one you provided
# and you want to extract the 'title', the first 'responses' element, 'mistral_response', 'faclon_response', and 'llama2_response'
rows = []
for key, value in data.items():
    row = {
        'title': value['title'],
        'responses': value['responses'][0],  # Taking only the first element of the responses list
        'mistral': value['mistral_response'],
        'falcon': value['faclon_response'],
        'llama2': value['llama2_response']
    }
    rows.append(row)

# Step 3: Create a DataFrame
df = pd.DataFrame(rows)

# Step 4: Export the DataFrame to an Excel file
excel_file_path = 'reddit_data.xlsx'
df.to_excel(excel_file_path, index=False)

print(f'Data has been successfully exported to {excel_file_path}.')
