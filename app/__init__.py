from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import logging
from logging.handlers import RotatingFileHandler

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

# Create logger
logger = logging.getLogger('webserver')
logger.setLevel(logging.INFO)

# Create a rotating file handler
handler = RotatingFileHandler('webserver.log', maxBytes=10000, backupCount= 10)
handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

webserver.logger = logger

from app import routes
