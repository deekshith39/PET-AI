from dateutil.parser import parse
import pandas as pd
import datetime
import re

from bank_statement_parser.config.constants import NULL_VALUES, GENERIC_LABELS, StandardHeader
from bank_statement_parser.config.patterns import GENERIC_PATTERNS, bank_abbreviations, noise_patterns
from bank_statement_parser.utils.logger import logger


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

    @classmethod
    def validate_and_extract_transactions(cls, data_df: pd.DataFrame, actual_to_standard: dict,
                                          file_name: str) -> pd.DataFrame | None:
        """Validates individual transaction rows and extracts valid ones."""
        try:
            date_col = [col for col, std in actual_to_standard.items() if std == StandardHeader.DATE.value][0]
            desc_col = [col for col, std in actual_to_standard.items() if std == StandardHeader.DESCRIPTION.value][0]
            credit_col = [col for col, std in actual_to_standard.items() if std == StandardHeader.CREDIT.value][0]
            debit_col = [col for col, std in actual_to_standard.items() if std == StandardHeader.DEBIT.value][0]
        except IndexError:
            logger.error(f"Missing essential columns for validation in {file_name}.")
            return None

        valid_rows_list = []
        for _, row in data_df.iterrows():
            date_val = row[date_col]
            desc_val = row[desc_col]
            credit_val = row[credit_col]
            debit_val = row[debit_col]

            # Validate individual fields. If any primary validation fails, skip or break.
            # Using 'and' for all checks means all must pass for a row to be considered valid
            if (TransactionValidator.is_valid_date(date_val) and
                    TransactionValidator.is_valid_description(desc_val) and
                    (TransactionValidator.is_valid_amount(credit_val) or TransactionValidator.is_valid_amount(
                        debit_val))):
                valid_rows_list.append(row)
            else:
                logger.debug(
                    f"Skipping invalid row in {file_name}: Date: {date_val}, Desc: {desc_val}, Credit: {credit_val}, Debit: {debit_val}")

        if not valid_rows_list:
            return None

        return pd.DataFrame(valid_rows_list, columns=data_df.columns)
