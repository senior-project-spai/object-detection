import logging

# Create __main__ logger
logger = logging.getLogger("__main__")

# Create handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)

