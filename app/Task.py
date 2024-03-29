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

        for state in response_dict:
            response_dict[state] = sum(response_dict[state]) / len(response_dict[state])

        if self.webserver.data_ingestor.question_answer_best_is_min(self.data['question']):
            response_dict = dict(sorted(response_dict.items(), key=lambda item: item[1]))
        else:
            response_dict = dict(sorted(response_dict.items(), key=lambda item: item[1], reverse=True))
        
        # sleep for 5 seconds
        #time.sleep(5)
        return response_dict


class StateMeanTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):
        total_sum = 0
        total_count = 0

        for dict_entry in self.list_of_dict:
            if dict_entry['Question'] == self.data['question'] and dict_entry["LocationDesc"] == self.data['state']:
                total_sum += float(dict_entry['Data_Value'])
                total_count += 1

        mean = total_sum / total_count

        return {self.data["state"]: mean}

class BestFiveTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):
        response_dict = StatesMeanTask(self.webserver.job_counter, self.data, self.webserver).solve()
        return dict(list(response_dict.items())[:5])

class WorstFiveTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):
        response_dict = StatesMeanTask(self.webserver.job_counter, self.data, self.webserver).solve()
        reversed_dict = dict(reversed(list(response_dict.items())))
        last_five_entries = dict(list(reversed_dict.items())[:5])
        return last_five_entries
    

class GlobalMeanTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):

        total_sum = 0
        total_count = 0

        for dict_entry in self.list_of_dict:
            if dict_entry['Question'] == self.data['question']:
                total_sum += float(dict_entry["Data_Value"])
                total_count += 1

        mean = total_sum / total_count

        return {"global_mean": mean}


class DiffFromMeanTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):

        total_sum = 0
        total_count = 0

        for dict_entry in self.list_of_dict:
            if dict_entry['Question'] == self.data['question']:
                total_sum += float(dict_entry["Data_Value"])
                total_count += 1

        mean = total_sum / total_count

        return {"global_mean": mean}