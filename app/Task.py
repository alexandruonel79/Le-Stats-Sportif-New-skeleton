from abc import ABC, abstractmethod

import time 

class Task(ABC):
    def __init__(self, id, data, list_of_dict):
        self.data = data
        self.id = id
        self.list_of_dict = list_of_dict
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

    @abstractmethod
    def solve(self):
        pass

class StatesMeanTask(Task):
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

    def calculate_mean(self, data_values_list: list) -> float:
        total_sum = 0 

        for val in data_values_list:
            total_sum += val
        
        return total_sum / len(data_values_list)

    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:
            if dict_entry['Question'] == self.data['question']:
                if dict_entry['LocationDesc'] in response_dict:
                    response_dict[dict_entry['LocationDesc']].append(float(dict_entry['Data_Value']))
                else:
                    response_dict[dict_entry['LocationDesc']] = [float(dict_entry['Data_Value'])]

        for state in response_dict:
            response_dict[state] = self.calculate_mean(response_dict[state])
        # if it's not in best is min it's the other way
        if self.data['question'] in self.questions_best_is_min:
            response_dict = dict(sorted(response_dict.items(), key=lambda item: item[1]))
        else:
            response_dict = dict(sorted(response_dict.items(), key=lambda item: item[1], reverse=True))
        
        # sleep for 5 seconds
        #time.sleep(5)
        return response_dict


class StateMeanTask(Task):
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

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
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

    def solve(self):
        response_dict = StatesMeanTask(self.id, self.data, self.list_of_dict).solve()
        return dict(list(response_dict.items())[:5])

class WorstFiveTask(Task):
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

    def solve(self):
        response_dict = StatesMeanTask(self.id, self.data, self.list_of_dict).solve()
        return dict(list(response_dict.items())[-5:])
    

class GlobalMeanTask(Task):
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

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
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

    def solve(self):
        global_mean_dict = GlobalMeanTask(self.id, self.data, self.list_of_dict).solve()
        global_mean = float(global_mean_dict["global_mean"])

        states_mean_dict = StatesMeanTask(self.id, self.data, self.list_of_dict).solve()

        response_dict = {}

        for state in states_mean_dict:
            response_dict[state] = global_mean - float(states_mean_dict[state])
        
        return response_dict


class StateDiffFromMeanTask(Task):
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

    def solve(self):
        global_mean_dict = GlobalMeanTask(self.id, self.data, self.list_of_dict).solve()
        global_mean = float(global_mean_dict["global_mean"])

        state_mean_dict = StateMeanTask(self.id, self.data, self.list_of_dict).solve()
        state_mean = float(state_mean_dict[self.data["state"]])
        
        res = global_mean - state_mean

        return {self.data["state"]: res} 
    

class MeanByCategoryTask(Task):
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:
            if dict_entry["Question"] != self.data["question"]:
                continue
            if dict_entry["StratificationCategory1"]:
                tuple_string = str((dict_entry["LocationDesc"], dict_entry["StratificationCategory1"], dict_entry["Stratification1"]))
                #print(f"Tuple string is {tuple_string}")
                if tuple_string not in response_dict:
                    response_dict[tuple_string] = [float(dict_entry["Data_Value"])]
                else:
                    response_dict[tuple_string].append(float(dict_entry["Data_Value"]))

        for key in response_dict:
            response_dict[key] = sum(response_dict[key]) / len(response_dict[key])
        
        return dict(sorted(response_dict.items()))


class StateMeanByCategoryTask(Task):
    def __init__(self, id, data, list_of_dict):
        super().__init__(id, data, list_of_dict)

    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:

            if dict_entry["Question"] != self.data["question"] or dict_entry["LocationDesc"] != self.data["state"]:
                continue

            if dict_entry["StratificationCategory1"]:
                tuple_string = str((dict_entry["StratificationCategory1"], dict_entry["Stratification1"]))
                #print(f"Tuple string is {tuple_string}")
                if tuple_string not in response_dict:
                    response_dict[tuple_string] = [float(dict_entry["Data_Value"])]
                else:
                    response_dict[tuple_string].append(float(dict_entry["Data_Value"]))

        for key in response_dict:
            response_dict[key] = sum(response_dict[key]) / len(response_dict[key])
        
        response_dict = dict(sorted(response_dict.items()))
        return {self.data["state"]: response_dict}


        