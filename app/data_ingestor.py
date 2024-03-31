import os
import json
from csv import DictReader

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        # https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/
        with open(csv_path, 'r') as f:
            dict_reader = DictReader(f)
    
            self.list_of_dict = list(dict_reader)
                    

    def get_list_of_dict(self):
        return self.list_of_dict

    def question_answer_best_is_min(self, question: str) -> bool:
        return question in self.questions_best_is_min

    def question_answer_best_is_max(self, question: str) -> bool:
        return question in self.questions_best_is_max