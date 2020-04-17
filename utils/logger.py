""" Custom Logger Class """
import logging


class Logger(object):
    """ Custom Logger Class """

    def __init__(self):
        """ Set up logger """
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s || [%(levelname)-8.8s] :: %(message)s')
        ch.setFormatter(formatter)
        logging.basicConfig(level=logging.DEBUG, handlers=[ch])
        self.test_log = logging.getLogger()
        # Shortcut commands
        self.err = self.error

    def debug(self, message, *args, **kwargs):
        """ log with DEBUG level """
        self.test_log.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """ log with INFO level """
        self.test_log.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """ log with WARNING level """
        self.test_log.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """ log with ERROR level """
        self.test_log.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """ log with CRITICAL level """
        self.test_log.critical(message, *args, **kwargs)


logger = Logger()
