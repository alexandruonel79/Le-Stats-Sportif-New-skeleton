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
        global_mean_dict = GlobalMeanTask(self.id, self.data, self.webserver).solve()
        global_mean = float(global_mean_dict["global_mean"])

        states_mean_dict = StatesMeanTask(self.id, self.data, self.webserver).solve()

        response_dict = {}

        for state in states_mean_dict:
            response_dict[state] = global_mean - float(states_mean_dict[state])
        
        return response_dict


class StateDiffFromMeanTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):
        global_mean_dict = GlobalMeanTask(self.id, self.data, self.webserver).solve()
        global_mean = float(global_mean_dict["global_mean"])

        state_mean_dict = StateMeanTask(self.id, self.data, self.webserver).solve()
        state_mean = float(state_mean_dict[self.data["state"]])
        
        res = global_mean - state_mean

        return {self.data["state"]: res} 
    

class MeanByCategoryTask(Task):
    def __init__(self, id, data, webserver):
        super().__init__(id, data, webserver)

    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:
            if dict_entry["Question"] != self.data["question"]:
                continue
            
            tuple_string = str((dict_entry["LocationDesc"], dict_entry["StratificationCategory1"], dict_entry["Stratification1"]))
            #print(f"Tuple string is {tuple_string}")
            if tuple_string not in response_dict:
                response_dict[tuple_string] = [float(dict_entry["Data_Value"])]
            else:
                response_dict[tuple_string].append(float(dict_entry["Data_Value"]))

        for key in response_dict:
            response_dict[key] = sum(response_dict[key]) / len(response_dict[key])
        
        return dict(sorted(response_dict.items()))