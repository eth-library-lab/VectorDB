import logging
class Logger():
    def __init__(self):
        logging.basicConfig(format='[%(levelname)s]: %(message)s',
                            level=logging.DEBUG)

    def debug(self, message: str):
        logging.debug(message)

    def info(self, message: str):
        logging.info(message)

    def warn(self, message: str):
        logging.warn(message)

    def error(self, message: str):
        logging.error(message)


logger = Logger()