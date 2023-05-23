import re
from datetime import datetime

class StatementInfo:
    def __init__(self):
        self.customerName = None
        self.accountNumber = None
        self.currency = None
        self.periodStart = None
        self.periodEnd = None
        self.openingBalance = None
        self.closingBalance = None
        self.totalDebit = None
        self.totalCredit = None
        self.transactions = []

class Transaction:
    def __init__(self):
        self.transactionDate = None
        self.amount = None
        self.balance = None
        self.type = None
        self.narration = None

    def haveData(self):
        if self.__dict__.keys():
            return True
        else:
            return False

def extract_bank_statement(statement_content):
    statement_info = StatementInfo()

    name_match = re.search(r"Account Name: (.+?) Account Number: (\d+)", statement_content)
    if name_match:
        customer_name = name_match.group(1).strip()
        account_number = name_match.group(2).strip()
        statement_info.customerName = customer_name
        statement_info.accountNumber = account_number

    currency_match = re.search(r"Currency: (\w+)", statement_content)
    if currency_match:
        currency = currency_match.group(1).strip()
        statement_info.currency = currency

    period_match = re.search(r"Period:\s+From (\d{2}-\w{3}-\d{4})\s+To (\d{2}-\w{3}-\d{4})", statement_content)
    if period_match:
        period_start = datetime.strptime(period_match.group(1), "%d-%b-%Y").isoformat()
        period_end = datetime.strptime(period_match.group(2), "%d-%b-%Y").isoformat()
        statement_info.periodStart = period_start
        statement_info.periodEnd = period_end

    transaction_matches = re.findall(r"(\d{2}-\w{3}-\d{4})\s(.+?)\s+(\d{2}-\w{3}-\d{4})\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)", statement_content)
    for match in transaction_matches:
        transaction = Transaction()
        transaction.transactionDate = datetime.strptime(match[0], "%d-%b-%Y").isoformat()
        transaction.narration = match[1].strip()
        debit = float(match[3].replace(",", ""))
        credit = float(match[4].replace(",", ""))
        transaction.balance = float(match[5].replace(",", ""))
        transaction.type = "debit" if debit > 0 else "credit"
        transaction.amount = debit if debit > 0 else credit

        statement_info.transactions.append(transaction)

    statement_info.openingBalance = statement_info.transactions[0].balance
    statement_info.closingBalance = statement_info.transactions[-1].balance

    total_debit = sum(transaction.amount for transaction in statement_info.transactions if transaction.type == "debit")
    total_credit = sum(transaction.amount for transaction in statement_info.transactions if transaction.type == "credit")

    statement_info.totalDebit = total_debit
    statement_info.totalCredit = total_credit

    return statement_info