import time
import logging

# create formatter
class UTCFormatter(logging.Formatter):
    converter = time.gmtime