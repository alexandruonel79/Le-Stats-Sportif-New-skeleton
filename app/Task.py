from abc import ABC, abstractmethod

import time 

class Task(ABC):
    def __init__(self, id, data, webserver):
        self.webserver = webserver
        self.data = data
        self.id = id
        self.list_of_dict = self.webserver.data_ingestor.get_list_of_dict()

    @abstractmethod
    def solve(self):
        pass

class StatesMeanTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:
            if dict_entry['Question'] == self.data['question']:
                if dict_entry['LocationDesc'] in response_dict:
                    response_dict[dict_entry['LocationDesc']].append(float(dict_entry['Data_Value']))
                else:
                    response_dict[dict_entry['LocationDesc']] = [float(dict_entry['Data_Value'])]
        
        
        # calculate and store mean for each state
        for state in response_dict:
            response_dict[state] = sum(response_dict[state]) / len(response_dict[state])
        # print the mean of Ohio for debugging purposes
        print(f"Mean of Ohio: {response_dict['Ohio']}")

        if self.webserver.data_ingestor.question_answer_best_is_min(self.data['question']):
            response_dict = dict(sorted(response_dict.items(), key=lambda item: item[1]))
        else:
            response_dict = dict(sorted(response_dict.items(), key=lambda item: item[1], reverse=True))
        
        # sleep for 5 seconds
        #time.sleep(5)
        return response_dict