from bank_statement_parser.config.constants import StandardHeader


def get_standard_header_keys():
    """
    Returns a list of all standard header keys as strings.
    Example: ['date', 'description', 'credit', 'debit']
    """
    return [header.value for header in StandardHeader]