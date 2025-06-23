from bank_statement_parser.config.constants import StandardHeader
import pandas as pd

def get_standard_header_keys():
    """
    Returns a list of all standard header keys as strings.
    Example: ['date', 'description', 'credit', 'debit']
    """
    return [header.value for header in StandardHeader if header.value != StandardHeader.AMOUNT.value]


def sanitize_numeric_column(series: pd.Series) -> pd.Series:
    """
    Cleans and converts a pandas Series to numeric type.
    Fills empty, null, or whitespace values with 0,
    and infers the appropriate numeric dtype.
    """
    return series.replace(['', ' ', None, pd.NA], 0).fillna(0).infer_objects()
