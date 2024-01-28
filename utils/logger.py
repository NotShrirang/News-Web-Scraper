import logging


def log_message(message: str, level: int):
    logging.basicConfig(filename='logger.log',
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO)

    if level == 1:
        logging.error(message)
    else:
        logging.info(message)
