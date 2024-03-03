import logging


def setup_logging():
    """
    Sets up basic logging configuration for the application.
    Logs will be written to app.log and output to the console.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app.log',
        filemode='a')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # Set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    # Add the handler to the root logger
    logging.getLogger('').addHandler(console)


def get_logger(name):
    """
    Returns a logger with the specified name.
    """
    return logging.getLogger(name)


setup_logging()
logger = get_logger(__name__)
