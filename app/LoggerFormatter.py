import time
import logging

# custom formatter for the gmt time
class UTCFormatter(logging.Formatter):
    converter = time.gmtime