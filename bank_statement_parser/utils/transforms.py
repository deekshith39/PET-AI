import re
import pandas as pd
import datetime
from dateutil.parser import parse


def mask_all_digits(text):
    """
    Masks long numeric sequences (e.g., card numbers, reference IDs) in a string.
    Replaces any sequence of 6 or more digits with asterisks.

    Args:
        text (str): Input string possibly containing sensitive numbers.

    Returns:
        str: Masked string with long digit sequences hidden.
    """
    if not isinstance(text, str):
        text = str(text)
    return re.sub(r"\d{6,}", lambda m: "*" * len(m.group()), text)


def normalize_date(value):
    """
    Converts various date formats into a consistent YYYY-MM-DD format.

    Args:
        value (any): A date-like object (string, Timestamp, or datetime).

    Returns:
        str: Normalized date string or the original value if parsing fails.
    """
    # If already a datetime-like object, format directly
    if isinstance(value, (pd.Timestamp, datetime.datetime)):
        return value.strftime("%Y-%m-%d")

    # Try parsing as string
    try:
        return parse(str(value), fuzzy=True).strftime("%Y-%m-%d")
    except Exception:
        print(f"⚠️ Failed to parse date from: {value}")
        return value  # Return original if parsing fails



