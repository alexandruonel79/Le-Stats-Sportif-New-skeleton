"""
    Module which stores the DataIngestor class
"""
from csv import DictReader

class DataIngestor:
    """
    DataIngestor class performs the reading of the csv and returns a list of dictionaries
    """
    def __init__(self, csv_path: str):
        with open(csv_path, 'r', encoding='utf-8') as f:
            # read the csv as a list of dictionaries
            dict_reader = DictReader(f)
            self.list_of_dict = list(dict_reader)

    def get_list_of_dict(self) -> list:
        """
        Returns:
            list of dictionaries
        """
        return self.list_of_dict
    