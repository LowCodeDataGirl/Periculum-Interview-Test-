
#  Bank Statement Parser

This Python program parses bank transactions from a given JSON file and extracts specific transaction data. It also pulls additional meaningful information from the bank statement sample provided.

## Getting Started
In order to run the solution, follow the instructions below:

### Prerequisites

- Python (3.6 or higher)
- JSON module (built-in with python)
- Datetime module (built-in with python)
- re module (built-in with python)
- os module (built-in with python)

## Problem
The aim of this project is to parse individual transactions from a bank statement JSON file. For each transaction, the following elements need to be extracted:

- Transaction date
- Transaction description
- Amount
- Type (credit or debit)
- Balance

The extracted data should be organized into a dictionary corresponding to the transaction. Additional information, including the customer name and account number, are also extracted.


 
## Directory Structure

To structure my solution, I organized the project directory as follows:

```- root
  ├── extract.py
  ├── run.py
  ├── output
  │   └── output.json
  └── src
      ├── bank_statement_sample.json
      ├── variables.py
      └── expected_output.json
```



## File Descriptions

- **extract.py:** The main script that contains the functions for extracting the transactions and loading all records into a nested dict object, which can then be dumped into a JSON file.

- **run.py:** Implements the solution to generate the required output.
- **output/:** Folder to dump the output JSON file. This is created if it does not exist.
- **src/:** The source folder containing the JSON files provided for this test.

  - **bank_statement_sample.json:** This is the JSON file containing extracted transactions from a PDF bank statement.

  - **variables.py:** Contains two classes with variables relevant to the statement records. StatementInfo class pertains to general information about the statement, while the Transaction class pertains to information about each transaction in the statement.

  - **expected_output.json:** Demonstrates the expected format for the output of your solution.
 
 



## Functionality
The main functionality of this project is to parse bank statement data from a JSON file and extract detailed information about the transactions and other details present in the statement. The data is formatted into a structure as required by the problem statement and then saved to an output JSON file.

The program does the following:

- Parses the provided JSON bank statement.
- Extracts each transaction's details and stores them in the Transaction class.
- Extracts general statement information such as customer name, account number, etc., and stores them in the StatementInfo class.
- Writes this information in a very specific format into an output JSON file.
- The transaction date for each transaction is converted to a datetime object in the format YYYY-MM-DDTHH:MM:SS (e.g., 2022-08-27T00:00:00). The transactions, along with other information, are stored in a nested dict object and dumped into a JSON file.

The output JSON is stored in the output folder. Please make sure to study the variables.py file carefully to understand the variables used in the classes.

To run the program, execute run.py. This will generate the required output and dump it into the output JSON file.

## Issue

- The current implementation of the run.py script takes a hardcoded string as the bank statement content, which is then passed to the extract_bank_statement function. This approach is not flexible or scalable, as it doesn't allow processing data from different JSON files.

- The provided code solves the problem of extracting information from a bank statement, but it does so without utilizing the provided StatementInfo and Transaction classes. Instead, it relies on dictionaries to store the extracted information. This implementation approach is suboptimal and can be improved by utilizing the provided classes appropriately.

## Expected Behavior
- The script should be able to load bank statement content from a JSON file dynamically.
- Initialize the StatementInfo class and populate its variables with the extracted general information from the bank statement.
- Initialize the Transaction class for each transaction in the bank statement and populate its variables with the relevant transaction details.


**Thank you for reading through this README**


## Check out this Cool Regex Generator

Hey there !. Check out this cool Regex Generator I made using OpenAI API and Retool [here](https://lowcodedatagirl.retool.com/apps/971a2010-f633-11ed-950e-830646754ab4/Regex%20Made%20Easy "Regex Generator with OpenAI API and retool")  


 **頑張って (Ganbatte)**



