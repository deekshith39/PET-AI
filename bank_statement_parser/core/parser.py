import os
import pandas as pd

from bank_statement_parser.config.constants import StandardHeader
from bank_statement_parser.core.file_loader import robust_load
from bank_statement_parser.core.header_detector import HeaderDetector
from bank_statement_parser.utils.common_utils import get_standard_header_keys
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
        Parses all files in the input directory, extracts valid transactions,
        normalizes them, and consolidates into a single CSV.
        """
        all_valid_rows = []

        logger.info(f"Scanning directory: {self.input_dir}")

        for file in os.listdir(self.input_dir):
            logger.info(f"Found file: {file}")

            if not file.endswith(('.xls', '.xlsx', '.csv')):
                logger.debug(f"Skipping unsupported file: {file}")
                continue

            file_path = os.path.join(self.input_dir, file)

            try:
                df = robust_load(file_path)

                if df is None or df.empty:
                    logger.warning(f"Skipping {file}: No data loaded.")
                    continue

                header_idx = HeaderDetector.find_best_header(df)
                if header_idx is None:
                    logger.warning(f"Skipping {file}: No header detected.")
                    continue

                headers = [str(col).strip() for col in df.iloc[header_idx].tolist()]
                data_df = df.iloc[header_idx + 1:].reset_index(drop=True)
                data_df.columns = headers

                logger.info(f"Header detected at row {header_idx}: {headers}")

                actual_to_standard = HeaderDetector.match_expected_to_actual(data_df.columns)
                logger.info(f"Column mapping: {actual_to_standard}")

                valid_rows = [
                    row for _, row in data_df.iterrows()
                    if TransactionValidator.is_valid_transaction_row(row)
                ]

                if not valid_rows:
                    logger.warning(f"No valid transactions in {file}")
                    continue

                partial_df = pd.DataFrame(valid_rows, columns=data_df.columns)[list(actual_to_standard.keys())]
                partial_df = partial_df.rename(columns=actual_to_standard)

                partial_df[StandardHeader.DESCRIPTION.value] = partial_df[StandardHeader.DESCRIPTION.value].astype(str).apply(mask_all_digits)
                partial_df[StandardHeader.DATE.value] = partial_df[StandardHeader.DATE.value].apply(normalize_date)

                partial_df = partial_df[get_standard_header_keys()]

                logger.info(f"Processed {file}: {len(partial_df)} valid rows")
                all_valid_rows.append(partial_df)

            except Exception as e:
                logger.exception(f"Error processing file {file}: {e}")
                continue
            # Line break for better readability in logs
            print()

        if not all_valid_rows:
            logger.warning("No valid transactions found across all files.")
            return

        final_df = pd.concat(all_valid_rows, ignore_index=True)
        final_df.to_csv(self.output_file, index=False)
        logger.info(f"Consolidated {len(final_df)} rows into: {self.output_file}")
