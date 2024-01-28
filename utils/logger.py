import logging


def log_message(message: str, level: int):
    logging.basicConfig(filename='logger.log',
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO)

    if level == 1:
        logging.error(message)
    else:
        logging.info(message)

    # try:
    #     with open('scraper.log', 'a') as f:
    #         f.write(message)
    # except Exception as e:
    #     with open('scraper.log', 'a') as f:
    #         f.write('Error: ' + str(e.args) + '\n')
