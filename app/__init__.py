"""
    Initialise the flask application, create the 'results' directory
"""

import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.logger import logger

webserver = Flask(__name__)
# create the directory if it doesn't exist
if not os.path.exists("results"):
    os.makedirs("results")

webserver.tasks_runner = ThreadPool()

webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1
# set the logger, alternative: using logger with a global variable
# which seems better, but global variables are forbidden
webserver.logger = logger

from app import routes

