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



# Bank statement content
statement_content = "\n\n\n\n\nElectronic Statement of Account\n…our bank\n\nType:\nthrough\nOverdraft\nDate | Time:                             30/04/2018\n\nAccount Name:   ARBITRARY NAME Account Number: 3189014610-0 \n\nCurrency:\n\nNGN  \n\nProduct: CURRENT LIMITED LIABILITY CO.ORDINARY\n\nPeriod:       From 01-04-2017      To 29-04-2018 PAGE: 1 of 35\n\nEntry Date Description  Value Date  Debit   Credit  Balance\n\n 1,698,671.30Opening Balance\n\n01-Apr-2017 Balance BF 01-Apr-2017          1,698,671.30 \n\n03-Apr-2017 Atm Withdrawal @10571001-Zib Ogudu Branch       U 01-Apr-2017  20,000.00      1,678,671.30 \n\n03-Apr-2017 Atm Withdrawal @10571001-Zib Ogudu Branch       U 01-Apr-2017  20,000.00      1,658,671.30 \n\n03-Apr-2017 Atm Withdrawal @10571003-Ogudu Branch Atm3      U 01-Apr-2017  20,000.00      1,638,671.30 \n\n03-Apr-2017 Atm Withdrawal Rev @10571001-Zib Ogudu Branch 01-Apr-2017      20,000.00  1,658,671.30 \n\n03-Apr-2017 Atm Withdrawal @10501013-Ebn000000001011 Ebn Og O03-Apr-2017  20,000.00      1,638,671.30 \n\n04-Apr-2017 Cob Transfer To Okanlawan  **6996 Cement Fbn 04-Apr-2017  400,000.00      1,238,671.30 \n\n04-Apr-2017 Cob Transfer To Okanlawan  **6996 Cement Fbn 04-Apr-2017  100.00      1,238,571.30 \n\n04-Apr-2017 Cob Transfer To Okanlawan  **6996 Cement Fbn 04-Apr-2017  5.00      1,238,566.30 \n\n04-Apr-2017 Sms Alert Charges 27-31mar 17 04-Apr-2017  24.00      1,238,542.30 \n\n05-Apr-2017 Atm Withdrawal @1050c029-Ebn00000000c027 Eng La L05-Apr-2017  20,000.00      1,218,542.30 \n\n05-Apr-2017 Atm Withdrawal @1050c029-Ebn00000000c027 Eng La L05-Apr-2017  65.00      1,218,477.30 \n\n05-Apr-2017 Atm Withdrawal Rev @1050c029-Ebn00000000c027 Eng05-Apr-2017      65.00  1,218,542.30 \n\n05-Apr-2017 Atm Withdrawal Rev @1050c029-Ebn00000000c027 Eng05-Apr-2017      20,000.00  1,238,542.30 \n\n05-Apr-2017 Atm Withdrawal @10331178-1033117804734 Shoprite I 05-Apr-2017  10,000.00      1,228,542.30 \n\n05-Apr-2017 Atm Withdrawal @10331178-1033117804734 Shoprite I 05-Apr-2017  65.00      1,228,477.30 \n\n05-Apr-2017 Atm Withdrawal @10331178-1033117804734 Shoprite I 05-Apr-2017  65.00      1,228,412.30 \n\n05-Apr-2017 Atm Withdrawal @10331178-1033117804734 Shoprite I 05-Apr-2017  10,000.00      1,218,412.30 \n\n05-Apr-2017 Cob Transfer To Omoregie J **2114 From Frank Abn 05-Apr-2017  7,000.00      1,211,412.30 \n\n05-Apr-2017 Cob Transfer To Omoregie J **2114 From Frank Abn 05-Apr-2017  100.00      1,211,312.30 \n\n05-Apr-2017 Cob Transfer To Omoregie J **2114 From Frank Abn 05-Apr-2017  5.00      1,211,307.30 \n\n10-Apr-2017 Sms Alert Charges 01-07apr 17 10-Apr-2017  204.00      1,211,103.30 \n\n11-Apr-2017 Atm Withdrawal @10503502-Ebn000000003501 Eng La L11-Apr-2017  20,000.00      1,191,103.30 \n\n11-Apr-2017 Atm Withdrawal @10503502-Ebn000000003501 Eng La L11-Apr-2017  65.00      1,191,038.30 \n\n11-Apr-2017 Atm Withdrawal @10503502-Ebn000000003501 Eng La L11-Apr-2017  20,000.00      1,171,038.30 \n\n11-Apr-2017 Atm Withdrawal @10503502-Ebn000000003501 Eng La L11-Apr-2017  65.00      1,170,973.30 \n\n12-Apr-2017 Transfer From Passmark Comms Ltd 12-Apr-2017      315,000.00  1,485,973.30 \n\n12-Apr-2017 Cbn Stamp Duty Charge - S1367771 12-Apr-2017  50.00      1,485,923.30 \n\n13-Apr-2017 Transfer From Anthony Omoregie 13-Apr-2017      400,000.00  1,885,923.30 \n\nView your statement online"

# Extract bank statement information
statement_info = extract_bank_statement(statement_content)

# Output folder path
output_folder = "output"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Output file path
output_file = os.path.join(output_folder, "output.json")

# Dump the output JSON to a file
with open(output_file, "w") as file:
    json.dump(statement_info, file, indent=4)

print("Extraction completed. Output JSON dumped to", output_file)


 
