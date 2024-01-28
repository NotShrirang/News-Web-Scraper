def log_message(message: str):
    try:
        with open('scraper.log', 'a') as f:
            f.write(message)
    except Exception as e:
        with open('scraper.log', 'a') as f:
            f.write('Error: ' + str(e.args) + '\n')
