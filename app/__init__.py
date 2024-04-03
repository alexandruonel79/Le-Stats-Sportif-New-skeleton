from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.logger import logger

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

webserver.logger = logger

from app import routes
