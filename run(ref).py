# This function reads a JSON file from the given file path.
def read_json_file(file_path):
    # Opening the file in 'read' mode.
    with open(file_path, 'r') as file:
        # Using json.load to parse the JSON file into a Python dictionary.
        data = json.load(file)
    # It returns the 'content' key from the dictionary. 
    # If 'content' does not exist, it will throw an error.
    return data['content']

# Path to the input JSON file.
input_json_path = "src/bank_statement_sample.json"  # Replace with your actual path

# Read the bank statement content from the JSON file using the defined function.
# The data is assumed to be under the 'content' key in the JSON file.
statement_content = read_json_file(input_json_path)

# Now we extract the actual bank statement information from the content we just read.
# It's not clear what this function does from this snippet.
statement_info = extract_bank_statement(statement_content)

# Define the output folder path where the result JSON will be stored.
output_folder = "output"

# Creates the output folder if it doesn't already exist.
# The 'exist_ok' parameter is set to True, which means Python will not throw an error if the folder already exists.
os.makedirs(output_folder, exist_ok=True)

# Defines the path for the output JSON file. It is in the output folder and the name of the file is 'output.json'.
output_file = os.path.join(output_folder, "output.json")

# Opens the output file in 'write' mode.
with open(output_file, "w") as file:
    # Dumps the statement_info object into the output file as JSON.
    # Uses a lambda function to handle objects not serializable by default json.
    # The 'indent' parameter is set to 4, which means the output JSON will be pretty-printed with an indentation of 4 spaces.
    json.dump(statement_info.__dict__, file, default=lambda o: o.__dict__, indent=4)

# Prints out a success message with the path of the output file.
print("Extraction completed. Output JSON dumped to", output_file)
