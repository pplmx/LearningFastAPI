import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    custom_format = logging.Formatter('%(asctime)s %(levelname)s\t'
                                      '%(pathname)s def %(funcName)s:%(lineno)d - %(message)s')

    cli_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('learning.log', encoding='utf-8')

    cli_handler.setFormatter(custom_format)
    file_handler.setFormatter(custom_format)

    cli_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    logger.handlers.clear()
    logger.addHandler(cli_handler)
    logger.addHandler(file_handler)
    return logger
