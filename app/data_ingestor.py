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
                    
            self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def get_list_of_dict(self):
        return self.list_of_dict

    def question_answer_best_is_min(self, question: str) -> bool:
        return question in self.questions_best_is_min

    def question_answer_best_is_max(self, question: str) -> bool:
        return question in self.questions_best_is_max