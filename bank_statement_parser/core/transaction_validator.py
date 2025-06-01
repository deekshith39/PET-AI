from dateutil.parser import parse
import pandas as pd
import datetime
import re

from bank_statement_parser.config.constants import NULL_VALUES, GENERIC_LABELS
from bank_statement_parser.config.patterns import GENERIC_PATTERNS, bank_abbreviations, noise_patterns


class TransactionValidator:
    # -----------------------------
    # Field Validators
    # -----------------------------
    @staticmethod
    def is_valid_date(value):
        """Check if the value is a recognizable date."""
        if isinstance(value, (pd.Timestamp, datetime.datetime)):
            return True
        if isinstance(value, (int, float)):
            return False
        if not isinstance(value, str):
            return False

        value = value.strip().lower()
        if value in NULL_VALUES:
            return False

        try:
            parse(value, fuzzy=True)
            return True
        except Exception:
            return False

    @staticmethod
    def is_valid_amount(value):
        """Check if the value is a valid number (float or int)."""
        try:
            val = float(value)
            return not pd.isna(val) and str(value).lower() not in NULL_VALUES
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_description(value):
        """Check if the value is a meaningful transaction description."""
        if not isinstance(value, str):
            return False

        value = value.strip().lower()

        # Remove known noise patterns
        if any(re.search(pattern, value, re.IGNORECASE) for pattern in noise_patterns):
            return False

        if value in NULL_VALUES or value in GENERIC_LABELS:
            return False

        if any(re.match(pattern, value) for pattern in GENERIC_PATTERNS):
            return False

        contains_abbreviation = any(abbrev.lower() in value for abbrev in bank_abbreviations)
        return contains_abbreviation or any(c.isalpha() for c in value)

    @classmethod
    def find_first_transaction_row(cls, df):
        """Find the first row in the DataFrame that contains a valid transaction."""
        for i, row in df.iterrows():
            if cls.is_valid_transaction_row(row):
                return i
        return None

    # -----------------------------
    # Row Validator
    # -----------------------------
    @classmethod
    def is_valid_transaction_row(cls, row=None):
        """Check if the row contains a valid transaction (date, amount, and description all distinct)."""
        if row is None:
            return False

        values = row.astype(str).tolist()
        non_empty_values = [val.strip() for val in values if val.strip().lower() not in NULL_VALUES]

        if len(non_empty_values) < 3:
            return False

        # Extract individual components
        date_val = next((val for val in non_empty_values if cls.is_valid_date(val)), None)
        amount_val = next((val for val in non_empty_values if cls.is_valid_amount(val)), None) # credit or debit
        desc_val = next((val for val in non_empty_values if cls.is_valid_description(val)), None)

        if not (date_val and amount_val and desc_val):
            return False

        # Ensure they are not overlapping values
        return len({str(date_val), str(amount_val), str(desc_val)}) == 3
