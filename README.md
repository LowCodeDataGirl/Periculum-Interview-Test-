
# Periculum Interview Test Solution

This repository contains my solution to the Periculum interview test. The objective of the test is to parse individual transactions from a JSON file extracted from a PDF bank statement. The goal is to extract relevant information such as transaction date, description, amount, type (credit or debit), and balance for each transaction, and organize them into a dictionary structure that matches the provided expected output format.

## Understanding the Test Questions

To start, I carefully reviewed the provided test questions and files. The `bank_statement_sample.json` file contains the extracted transactions from a PDF bank statement. The `variables.py` file provides two classes: `StatementInfo` and `Transaction`, which define the variables relevant to the statement records. The `expected_output.json` file outlines the expected format for the solution output.

## Project Structure

To structure my solution, I organized the project directory as follows:

```
- extract.py
- run.py
- output/
- src/
  - bank_statement_sample.json
  - variables.py
  - expected_output.json
```

- `extract.py`: This script contains the functions for extracting the transactions and loading all records into a nested dictionary object, which can then be dumped into a JSON file.
- `run.py`: This script implements the solution to generate the required output by utilizing the functions defined in `extract.py`.
- `output/`: This folder is used to store the output JSON file.
- `src/`: This folder contains the provided files for the test.
  - `bank_statement_sample.json`: This file contains the JSON data extracted from a PDF bank statement.
  - `variables.py`: This file defines the `StatementInfo` and `Transaction` classes with relevant variables for the statement records.
- `expected_output.json`: This file specifies the expected format for the output JSON.

## Solution Approach

Based on the test questions and provided files, I proceeded with the following approach:

1. I created the `load_data` function in `extract.py` to read the content of the JSON file and return it as a string.
2. I implemented the `extract_account_info` function to extract relevant account information, such as account name, account number, currency, and period, from the content of the JSON file using regular expressions.
3. I used the `datetime.strptime` method to convert the period start and end dates from the extracted information to datetime objects in the format `YYYY-MM-DDTHH:MM:SS`.
4. With the extracted account information, I instantiated the `StatementInfo` class with the relevant variables and created an instance called `statement_info`.
5. Next, I implemented the `extract_transactions` function to extract individual transactions from the content of the JSON file using regular expressions.
6. I looped over the extracted transactions and processed each transaction individually.
7. Inside the loop, I parsed the transaction date, description, value date, debit, credit, and balance using regular expressions.
8. I used `datetime.strptime` to convert the transaction date and value date strings to datetime objects in the format `YYYY-MM-DDTHH:MM:SS`.
9. I removed commas from the debit, credit, and balance amounts and converted them to float values.
10. For each transaction, I instantiated the `Transaction` class and assigned the extracted values to the relevant variables.
11. Finally, I added the instantiated `Transaction` object to the list of transactions in the `StatementInfo` instance.
12. In the `main` function, I utilized the above-defined functions to load the JSON data, extract the account information, extract the transactions, and create the final `StatementInfo` object.
13. I converted the `StatementInfo` instance to a dictionary using the `to_dict()` method, and then