import os
import pandas as pd

from bank_statement_parser.config.constants import StandardHeader
from bank_statement_parser.core.file_loader import robust_load
from bank_statement_parser.core.header_detector import HeaderDetector
from bank_statement_parser.utils.common_utils import get_standard_header_keys, sanitize_numeric_column
from bank_statement_parser.utils.logger import logger
from bank_statement_parser.core.transaction_validator import TransactionValidator
from bank_statement_parser.utils.transforms import mask_all_digits, normalize_date


class BankStatementParser:

    def __init__(self, input_dir, output_file):
        """
        Initializes the parser with input directory and output file path.
        """
        self.input_dir = input_dir
        self.output_file = output_file

    def process(self):
        """
        Orchestrates the entire transaction processing pipeline.
        Parses all supported files in the input directory, extracts and
        validates transactions, normalizes them, and consolidates into a single CSV.
        """
        all_valid_rows = []
        logger.info(f"Scanning directory: {self.input_dir}")

        for file_name in os.listdir(self.input_dir):
            file_path = os.path.join(self.input_dir, file_name)
            logger.info(f"Processing file: {file_name}")

            if not file_name.endswith(('.xls', '.xlsx', '.csv')):
                logger.debug(f"Skipping unsupported file: {file_name}")
                continue

            try:
                processed_df = self.process_single_file(file_path, file_name)
                if processed_df is not None:
                    all_valid_rows.append(processed_df)
            except Exception as e:
                logger.exception(f"Error processing file {file_name}: {e}")
            print()  # For readability in logs

        self.consolidate_and_save(all_valid_rows)

    def process_single_file(self, file_path: str, file_name: str) -> pd.DataFrame | None:
        """
        Processes a single transaction file.

        Loads the file, detects headers, validates and normalizes transactions.

        Args:
            file_path (str): The full path to the file.
            file_name (str): The name of the file.

        Returns:
            pd.DataFrame | None: A DataFrame of processed and normalized transactions
                                 if successful, otherwise None.
        """
        df = robust_load(file_path)

        if df is None or df.empty:
            logger.warning(f"Skipping {file_name}: No data loaded or file is empty.")
            return None

        header_idx = HeaderDetector.find_best_header(df)
        if header_idx is None:
            logger.warning(f"Skipping {file_name}: No header detected.")
            return None

        headers = [str(col).strip() for col in df.iloc[header_idx].tolist()]
        data_df = df.iloc[header_idx + 1:].reset_index(drop=True)
        data_df.columns = headers
        logger.info(f"Header detected at row {header_idx}: {headers}")

        actual_to_standard = HeaderDetector.match_expected_to_actual(data_df.columns)
        logger.info(f"Column mapping: {actual_to_standard}")

        if not actual_to_standard:
            logger.warning(f"Skipping {file_name}: Could not map essential columns to standard headers.")
            return None

        valid_transactions_df = TransactionValidator.validate_and_extract_transactions(data_df, actual_to_standard, file_name)
        if valid_transactions_df is None or valid_transactions_df.empty:
            logger.warning(f"No valid transactions found in {file_name}")
            return None

        normalized_df = self.normalize_transactions(valid_transactions_df, actual_to_standard)
        final_df = self.generate_net_amount_coulmn(normalized_df)

        logger.info(f"Processed {file_name}: {len(final_df)} valid rows")
        return final_df

    def generate_net_amount_coulmn(self, normalized_df) -> pd.DataFrame:
        """
        Calculates the net amount for each transaction by subtracting the debit value from the credit value.
        Ensures that credit and debit columns are properly converted to floats, handling missing or invalid values.

        Args:
            normalized_df (pd.DataFrame): DataFrame containing at least CREDIT and DEBIT columns.

        Returns:
            pd.DataFrame: The input DataFrame with an additional AMOUNT column representing net amount.
        """
        normalized_df[StandardHeader.CREDIT.value] = (
            normalized_df[StandardHeader.CREDIT.value]
            .infer_objects(copy=False)
            .replace(['', ' ', None], pd.NA)
            .fillna(0)
            .astype(float)
        )
        normalized_df[StandardHeader.DEBIT.value] = (
            normalized_df[StandardHeader.DEBIT.value]
            .infer_objects(copy=False)
            .replace(['', ' ', None], pd.NA)
            .fillna(0)
            .astype(float)
        )
        normalized_df[StandardHeader.AMOUNT.value] = (
                normalized_df[StandardHeader.CREDIT.value] -
                normalized_df[StandardHeader.DEBIT.value]
        )
        return normalized_df

    def normalize_transactions(self, df_to_normalize: pd.DataFrame, actual_to_standard: dict) -> pd.DataFrame:
        """
        Normalizes the transaction data by renaming columns, masking sensitive data,
        and formatting dates.

        Args:
            df_to_normalize (pd.DataFrame): The DataFrame with validated transactions.
            actual_to_standard (dict): Mapping of actual column names to standard names.

        Returns:
            pd.DataFrame: The normalized DataFrame with standard headers.
        """
        # Select and rename columns to standard
        partial_df = df_to_normalize[list(actual_to_standard.keys())]
        partial_df = partial_df.rename(columns=actual_to_standard)

        # Apply normalization functions
        if StandardHeader.DESCRIPTION.value in partial_df.columns:
            partial_df[StandardHeader.DESCRIPTION.value] = partial_df[StandardHeader.DESCRIPTION.value].astype(
                str).apply(mask_all_digits)
        if StandardHeader.DATE.value in partial_df.columns:
            partial_df[StandardHeader.DATE.value] = partial_df[StandardHeader.DATE.value].apply(normalize_date)

        # Ensure consistent column order
        return partial_df[get_standard_header_keys()]

    def consolidate_and_save(self, all_valid_rows: list[pd.DataFrame]):
        """
        Consolidates all processed DataFrames and saves them to a single CSV file.

        Args:
            all_valid_rows (list[pd.DataFrame]): A list of DataFrames, each containing
                                                valid and normalized transactions from a file.
        """
        if not all_valid_rows:
            logger.warning("No valid transactions found across all files. No output file generated.")
            return

        final_df = pd.concat(all_valid_rows, ignore_index=True)
        final_df.to_csv(self.output_file, index=False)
        logger.info(f"Consolidated {len(final_df)} rows into: {self.output_file}")

