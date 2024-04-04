from csv import DictReader

class DataIngestor:
    def __init__(self, csv_path: str):
        with open(csv_path, 'r') as f:
            # read the csv as a list of dictionaries
            dict_reader = DictReader(f)
            self.list_of_dict = list(dict_reader)
                    
    def get_list_of_dict(self):
        return self.list_of_dict
