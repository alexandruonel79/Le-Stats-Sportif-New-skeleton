"""
    Module used to create the custom formatter to get the GMT time
"""

import time
import logging

class UTCFormatter(logging.Formatter):
    """
        Custom formatter for the gmt time
    """
    converter = time.gmtime
