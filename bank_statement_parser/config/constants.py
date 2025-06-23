from enum import Enum


class StandardHeader(Enum):
    DATE = "date"
    DESCRIPTION = "description"
    DEBIT = "debit"
    CREDIT = "credit"
    AMOUNT = "net_amount"

expected_headers = {
    StandardHeader.DATE: [
        "date", "txn date", "value date", "transaction date", "posting date", "tran date",
        "dt", "trans date", "process date", "effective date", "book date"
    ],
    StandardHeader.DESCRIPTION: [
        "description", "narration", "details", "particulars", "transaction details", "remark",
        "txn details", "transaction description", "purpose", "memo", "note", "comments"
    ],
    StandardHeader.DEBIT: [
        "debit", "withdrawal", "amount debited", "debit amount", "dr", "withdraw", "debit amt",
        "dr amount", "paid", "out", "payment", "disbursement"
    ],
    StandardHeader.CREDIT: [
        "credit", "deposit", "amount credited", "credit amount", "cr", "deposit amount", "credit amt",
        "cr amount", "received", "in", "receipt", "collection"
    ]
}

NULL_VALUES = {"", "nan"}
GENERIC_LABELS = {"date", "opening", "closing", "balance"}
# Maximum number of rows to scan above the first transaction row
HEADER_SCAN_RANGE = 3

