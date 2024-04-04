import logging
from logging.handlers import RotatingFileHandler
from app.LoggerFormatter import UTCFormatter
# inspired from documentation, the link from ocw
# https://docs.python.org/3/howto/logging.html

# create logger
logger = logging.getLogger("app.Log")
logger.setLevel(logging.INFO)

# create console handler and set level to info
# using the RotatingFileHandler
ch = RotatingFileHandler('webserver.log', maxBytes=100000, backupCount= 10)
ch.setLevel(logging.INFO)

# using my custom formatter, to use the GMT time
formatter = UTCFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)