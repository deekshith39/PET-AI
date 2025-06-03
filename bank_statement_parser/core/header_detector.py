from rapidfuzz import fuzz
from bank_statement_parser.config.constants import expected_headers, HEADER_SCAN_RANGE
from bank_statement_parser.core.transaction_validator import TransactionValidator
from bank_statement_parser.utils.logger import logger


class HeaderDetector:
    """
    A class to detect headers in a bank statement using fuzzy string matching.
    """

    @staticmethod
    def match_expected_to_actual(actual_headers):
        """
        Matches expected header categories (like 'date', 'credit', etc.) to the best-matching actual headers
        using fuzzy string matching.

        Returns:
            dict: A mapping of {actual_header: expected_key}, e.g. {'Txn Date': 'date'}
        """
        matches = []

        # Generate (expected_key, actual_header, score) for all combinations
        for expected_key, alias_list in expected_headers.items():
            for actual in actual_headers:
                score = max(fuzz.partial_ratio(actual.lower(), alias.lower()) for alias in alias_list)
                matches.append((expected_key.value, actual, score))

        # Sort matches by descending score
        matches.sort(key=lambda x: x[2], reverse=True)

        used_actual_headers = set()
        assigned_keys = set()
        intermediate_mapping = {}

        # Greedy matching
        for expected_key, actual, score in matches:
            if actual not in used_actual_headers and expected_key not in assigned_keys:
                intermediate_mapping[expected_key] = actual
                used_actual_headers.add(actual)
                assigned_keys.add(expected_key)

        # Flip mapping
        final_mapping = {actual: expected for expected, actual in intermediate_mapping.items()}
        return final_mapping

    @staticmethod
    def detect_header_above_row(df, start_row):
        """
        Scans a few rows above a given row index to find the most likely header row.

        Args:
            df (pd.DataFrame): Raw DataFrame (no headers).
            start_row (int): Index of the first transaction row.

        Returns:
            int or None: Best header row index or None.
        """
        best_idx = None
        best_score = -1

        for i in range(max(0, start_row - HEADER_SCAN_RANGE), start_row):
            row_cells = df.iloc[i].astype(str).str.lower().tolist()
            category_scores = []

            for expected_terms in expected_headers.values():
                term_score = max(
                    fuzz.partial_ratio(cell, expected_term)
                    for cell in row_cells
                    for expected_term in expected_terms
                )
                category_scores.append(term_score)

            avg_score = sum(category_scores) / len(category_scores)

            if avg_score > best_score:
                best_score = avg_score
                best_idx = i

        return best_idx

    @staticmethod
    def score_header_row(row_values):
        """
        Computes the average fuzzy match score of a row against all expected header groups.

        Args:
            row_values (List[str]): Values in the row.

        Returns:
            float: Average match score across all header groups.
        """
        total_score = 0
        category_count = 0

        for expected_terms in expected_headers.values():
            best_score = max(
                fuzz.partial_ratio(cell.lower(), term.lower())
                for cell in row_values
                for term in expected_terms
            )
            total_score += best_score
            category_count += 1

        return total_score / category_count if category_count > 0 else 0.0

    @staticmethod
    def find_best_header(df, scan_top_n=50):
        """
        Finds the best header row using both bottom-up and top-down strategies.

        Args:
            df (pd.DataFrame): Raw input DataFrame.
            scan_top_n (int): Number of top rows to scan for top-down strategy.

        Returns:
            int or None: Index of the best header row.
        """

        # Try to find the first valid transaction row
        first_transaction_index = TransactionValidator.find_first_transaction_row(df)

        bottom_up_score = -1
        bottom_up_header_index = None

        if first_transaction_index is not None:
            bottom_up_header_index = HeaderDetector.detect_header_above_row(df, first_transaction_index)
            bottom_up_values = df.iloc[bottom_up_header_index].astype(str).str.lower().tolist()
            bottom_up_values = [val for val in bottom_up_values if val.strip()]
            bottom_up_score = HeaderDetector.score_header_row(bottom_up_values)
            logger.debug(
                f"Bottom-up candidate row {bottom_up_header_index}: {df.iloc[bottom_up_header_index].tolist()} with score {bottom_up_score:.2f}")

        # Always run top-down strategy
        best_top_score = -1
        best_top_index = None
        for i in range(min(scan_top_n, len(df))):
            row = df.iloc[i].astype(str).str.lower().tolist()
            row = [val for val in row if val.strip()]
            score = HeaderDetector.score_header_row(row)

            if score > best_top_score:
                best_top_score = score
                best_top_index = i

        logger.debug(
            f"Top-down candidate row {best_top_index}: {df.iloc[best_top_index].tolist()} with score {best_top_score:.2f}")

        # If both are available, choose the better
        if bottom_up_header_index is not None and bottom_up_score >= best_top_score:
            logger.info("Selected Bottom-up header")
            return bottom_up_header_index
        else:
            logger.info("Selected Top-down header")
            return best_top_index

