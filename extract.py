import json
import re
from datetime import datetime
from src.variables import StatementInfo, Transaction

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def extract_account_info(content):
    # Define regex patterns
    account_name_pattern = r"Account Name:\s+([A-Z\s]+)"
    account_number_pattern = r"Account Number:\s+(\d+-\d+)"
    currency_pattern = r"Currency:\s+(\w+)"
    period_pattern = r"Period:\s+From\s+([\d\-]+)\s+To\s+([\d\-]+)"
    
    # Extract information
    account_name = re.search(account_name_pattern, content)[1]
    account_number = re.search(account_number_pattern, content)[1]
    currency = re.search(currency_pattern, content)[1]
    period_start, period_end = re.search(period_pattern, content).groups()
    
    # Convert dates to datetime objects and then to ISO format
    period_start = datetime.strptime(period_start, '%d-%m-%Y').isoformat()
    period_end = datetime.strptime(period_end, '%d-%m-%Y').isoformat()
    
    # Create a StatementInfo instance
    statement_info = StatementInfo(account_name, account_number, currency, period_start, period_end)
    
    return statement_info

def extract_transactions(content, statement_info):
    # Define regex pattern for transactions
    transaction_pattern = r"(\d{2}-\w{3}-\d{4})\s+(.*?)\s+(\d{2}-\w{3}-\d{4})\s+([\d,]*\.?\d{0,2})\s+([\d,]*\.?\d{0,2})?\s+([\d,]*\.?\d{0,2})"
    
    # Find all transactions in the content
    transactions = re.findall(transaction_pattern, content)

    # Extract information for each transaction and create a Transaction instance
    for transaction in transactions:
        transaction_date, description, value_date, debit, credit, balance = transaction
        transaction_date = datetime.strptime(transaction_date, '%d-%b-%Y').isoformat()
        value_date = datetime.strptime(value_date, '%d-%b-%Y').isoformat()
        
        # Remove commas from the amounts and convert them to floats
        debit = float(debit.replace(',', '')) if debit else 0.0
        credit = float(credit.replace(',', '')) if credit else 0.0
        balance = float(balance.replace(',', '')) if balance else 0.0
        
        # Create a Transaction instance and add it to the list of transactions in the StatementInfo instance
        transaction_info = Transaction(transaction_date, description, value_date, debit, credit, balance)
        statement_info.transactions.append(transaction_info)

   
                  
                  
                  
def main(file_path):
    # Load the data
    content = load_data(file_path)
    
    # Extract account information
    statement_info = extract_account_info(content)
    
    # Extract transactions
    extract_transactions(content, statement_info)
    
    # Convert the StatementInfo instance to a dict and dump it into a JSON file
    with open('output.json', 'w') as f:
        json.dump(statement_info.to_dict(), f, default=str, indent=4)

