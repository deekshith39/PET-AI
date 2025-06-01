import pandas as pd
import os


def robust_load(input_file):
    """
    Loads a bank statement file into a DataFrame based on its extension.

    Supports `.xlsx`, `.xls`, and `.csv` formats.

    Args:
        input_file (str): Path to the input file.

    Returns:
        pd.DataFrame: Loaded dataframe with no header assumed.

    Raises:
        ValueError: If file format is unsupported or reading fails.
    """
    _, ext = os.path.splitext(input_file)
    ext = ext.lower().lstrip('.')  # extract and normalize file extension

    if ext == "xlsx":
        return pd.read_excel(input_file, engine="openpyxl", header=None)

    elif ext == "xls":
        try:
            return pd.read_excel(input_file, engine="xlrd", header=None)
        except Exception as e:
            raise ValueError(f"⚠️ Error reading {input_file}: {e}")

    elif ext == "csv":
        return pd.read_csv(input_file, header=None)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
