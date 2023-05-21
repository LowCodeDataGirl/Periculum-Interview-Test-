import re
from datetime import datetime
import json
import os

def extract_bank_statement(statement_content):
    statement_info = {}

    # Extract customer name and account number
    name_match = re.search(r"Account Name: (.+?) Account Number: (\d+)", statement_content)
    if name_match:
        customer_name = name_match.group(1).strip()
        account_number = name_match.group(2).strip()
        statement_info["customerName"] = customer_name
        statement_info["accountNumber"] = account_number

    # Extract currency
    currency_match = re.search(r"Currency: (\w+)", statement_content)
    if currency_match:
        currency = currency_match.group(1).strip()
        statement_info["currency"] = currency

    # Extract period start and end
    period_match = re.search(r"Period:\s+From (\d{2}-\w{3}-\d{4})\s+To (\d{2}-\w{3}-\d{4})", statement_content)
    if period_match:
        period_start = period_match.group(1).strip()
        period_end = period_match.group(2).strip()
        statement_info["periodStart"] = datetime.strptime(period_start, "%d-%b-%Y").isoformat()
        statement_info["periodEnd"] = datetime.strptime(period_end, "%d-%b-%Y").isoformat()

    # Extract transactions
    transactions = []
    transaction_matches = re.findall(r"(\d{2}-\w{3}-\d{4})\s(.+?)\s+(\d{2}-\w{3}-\d{4})\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)", statement_content)
    for match in transaction_matches:
        transaction_date = datetime.strptime(match[0], "%d-%b-%Y").isoformat()
        narration = match[1].strip()
        debit = float(match[3].replace(",", ""))
        credit = float(match[4].replace(",", ""))
        balance = float(match[5].replace(",", ""))
        transaction_type = "debit" if debit > 0 else "credit"

        transaction = {
            "transactionDate": transaction_date,
            "narration": narration,
            "amount": debit if debit > 0 else credit,
            "balance": balance,
            "type": transaction_type
        }

        transactions.append(transaction)

    statement_info["openingBalance"] = transactions[0]["balance"]
    statement_info["closingBalance"] = transactions[-1]["balance"]

    # Calculate total debit and credit
    total_debit = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "debit")
    total_credit = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "credit")

    statement_info["totalDebit"] = total_debit
    statement_info["totalCredit"] = total_credit

    statement_info["transactions"] = transactions

    return statement_info
