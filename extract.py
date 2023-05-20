import json
import re
from datetime import datetime
from src.variables import StatementInfo, Transaction

# Function to load the data from the text file
def load_data(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

# Function to extract the account info from the statement data using regex
def extract_account_info(content):
    # Define regex patterns for various account information
    account_name_pattern = r"Account Name:\s+([A-Z\s]+)"
    account_number_pattern = r"Account Number:\s+(\d+-\d+)"
    currency_pattern = r"Currency:\s+(\w+)"
    period_pattern = r"Period:\s+From\s+([\d\-]+)\s+To\s+([\d\-]+)"
    
    # Use regex search function to find matches in the content
    account_name = re.search(account_name_pattern, content)[1]
    account_number = re.search(account_number_pattern, content)[1]
    currency = re.search(currency_pattern, content)[1]
    period_start, period_end = re.search(period_pattern, content).groups()
    
    # Convert dates from string to datetime objects and then to ISO format for standardization
    period_start = datetime.strptime(period_start, '%d-%m-%Y').isoformat()
    period_end = datetime.strptime(period_end, '%d-%m-%Y').isoformat()
    
    # Create a StatementInfo object and populate it with the extracted account information
    statement_info = StatementInfo(account_name, account_number, currency, period_start, period_end)
    
    return statement_info

# Function to extract transaction info from the statement data using regex
def extract_transactions(content, statement_info):
    # Define regex pattern for transactions
    transaction_pattern = r"(\d{2}-\w{3}-\d{4})\s+(.*?)\s+(\d{2}-\w{3}-\d{4})\s+([\d,]*\.?\d{0,2})\s+([\d,]*\.?\d{0,2})?\s+([\d,]*\.?\d{0,2})"
    
    # Find all transaction data in the content using the regex pattern
    transactions = re.findall(transaction_pattern, content)

    # Loop through each transaction and extract specific information
    for transaction in transactions:
        transaction_date, description, value_date, debit, credit, balance = transaction
        
        # Convert date from string to datetime object and then to ISO format
        transaction_date = datetime.strptime(transaction_date, '%d-%b-%Y').isoformat()
        value_date = datetime.strptime(value_date, '%d-%b-%Y').isoformat()
        
        # Remove commas from the amounts and convert them to floats for calculations
        debit = float(debit.replace(',', '')) if debit else 0.0
        credit = float(credit.replace(',', '')) if credit else 0.0
        balance = float(balance.replace(',', '')) if balance else 0.0
        
        # Create a Transaction object for each transaction and append it to the transactions list in the StatementInfo object
        transaction_info = Transaction(transaction_date, description, value_date, debit, credit, balance)
        statement_info.transactions.append(transaction_info)

# Main function to be executed when the script runs
def main(file_path):
    # Load the data from the file
    content = load_data(file_path)
    
    # Extract account information
    statement_info = extract_account_info(content)
    
    # Extract transactions
    extract_transactions(content, statement_info)
    
    # Convert the StatementInfo instance to a dict and save it into a JSON file for easy use in the future
    with open('output.json', 'w') as f:
        json.dump(statement_info.to_dict(), f, default=str, indent=4)
