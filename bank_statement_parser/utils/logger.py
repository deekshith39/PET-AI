
import logging

# Create a custom logger
logger = logging.getLogger("BankStatementParser")
logger.setLevel(logging.DEBUG)  # Set to INFO or WARNING in production

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)

# Add handlers to the logger
if not logger.hasHandlers():
    logger.addHandler(console_handler)
