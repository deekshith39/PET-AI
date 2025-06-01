noise_patterns = [
            r'statement\s+(of|for|period)',
            r'account\s+(holder|number|summary)',
            r'customer\s+(name|id|details)',
            r'address\s*:',
            r'phone\s*(no|number)\s*:',
            r'email\s*(id|address)\s*:',
            r'branch\s+(name|code|address)',
            r'ifsc\s*(code)?\s*:',
            r'opening\s+balance',
            r'closing\s+balance',
            r'total\s+(credit|debit|transactions)',
            r'summary\s+(of|for)',
            r'thank\s+you\s+for\s+banking',
            r'continued\s+(on|from)',
            r'page\s+\d+(\s+of\s+\d+)?',
            r'(generated|printed)\s+on\s*:',
            r'statement\s+period\s*:',
            r'customer\s+id\s*:',
            r'^\s*$',
            r'bank\s+(name|logo)',
            r'terms\s+(and|&)\s+conditions',
            r'disclaimer',
            r'important\s+notes?',
            r'legend\s*:',
            r'abbreviations?\s*:'
        ]

GENERIC_PATTERNS = [r"^(transaction|txn|narration|particulars|details|ref|id)[\s:]*$"]

# Bank Abbreviations and Their Meanings
# | Abbreviation | Meaning                                      |
# |--------------|----------------------------------------------|
# | NEFT         | National Electronic Funds Transfer           |
# | RTGS         | Real-Time Gross Settlement                   |
# | IMPS         | Immediate Payment Service                    |
# | UPI          | Unified Payments Interface                   |
# | ECS          | Electronic Clearing Service                  |
# | NACH         | National Automated Clearing House            |
# | ACH          | Automated Clearing House                     |
# | ATM          | Automated Teller Machine                     |
# | POS          | Point of Sale                                |
# | CHQ          | Cheque                                       |
# | CLG          | Clearing                                     |
# | TPT          | Third Party Transfer                         |
# | TRF          | Transfer                                     |
# | IB           | Internet Banking                             |
# | MB           | Mobile Banking                               |
# | VPA          | Virtual Payment Address (UPI)                |
# | BIL/BILLPAY  | Bill Payment                                 |
# | AUTOPAY      | Auto Debit for Bills                         |
# | SAL/SALARY   | Salary                                       |
# | DIV          | Dividend                                     |
# | INT          | Interest                                     |
# | TDS          | Tax Deducted at Source                       |
# | REF          | Refund                                       |
# | CHRG         | Charges                                      |
# | REV          | Reversal                                     |
# | PUR          | Purchase                                     |
# | CASHDEP      | Cash Deposit                                 |
# | CASHWDL      | Cash Withdrawal                              |
# | IB/IBFT      | Internet Banking Fund Transfer               |
# | MB/MOB       | Mobile Banking                               |
# | BBPS         | Bharat Bill Payment System                   |
# | CHQ NO.      | Cheque Number                                |
# | INST NO.     | Instrument Number                            |
# | TXN/TRAN     | Transaction                                  |
# | REF NO.      | Reference Number                             |
# | B/F          | Brought Forward                              |
# | C/F          | Carried Forward                              |
# | BOD          | Beginning of Day                             |
# | EOD          | End of Day                                   |
# | MIN BAL      | Minimum Balance                              |
# | AMB CHG      | Average Monthly Balance Charge               |

bank_abbreviations = {
    "NEFT",
    "RTGS",
    "IMPS",
    "UPI",
    "ECS",
    "NACH",
    "ACH",
    "ATM",
    "POS",
    "CHQ",
    "CLG",
    "TPT",
    "TRF",
    "IB",
    "MB",
    "VPA",
    "BIL/BILLPAY",
    "AUTOPAY",
    "SAL/SALARY",
    "DIV",
    "INT",
    "TDS",
    "REF",
    "CHRG",
    "REV",
    "PUR",
    "CASHDEP",
    "CASHWDL",
    "IB/IBFT",
    "MB/MOB",
    "BBPS",
    "CHQ NO.",
    "INST NO.",
    "TXN/TRAN",
    "REF NO.",
    "B/F",
    "C/F",
    "BOD",
    "EOD",
    "MIN BAL",
    "AMB CHG"
}