"""
    Module for the implementation of the tasks
"""

import logging
from abc import ABC, abstractmethod


class Task(ABC):
    """
    Abstract class for the tasks
    """

    def __init__(self, id, data, list_of_dict):
        self.data = data
        self.id = id
        self.list_of_dict = list_of_dict
        self.questions_best_is_min = [
            "Percent of adults aged 18 years and older who have an overweight classification",
            "Percent of adults aged 18 years and older who have obesity",
            "Percent of adults who engage in no leisure-time physical activity",
            "Percent of adults who report consuming fruit less than one time daily",
            "Percent of adults who report consuming vegetables less than one time daily",
        ]
        self.logger = logging.getLogger("app.Log")

    @abstractmethod
    def solve(self):
        """
        Abstract solve method
        """
        pass

    def calculate_mean(self, data_values_list: list) -> float:
        """
        Used to calculate the mean of a list of floats
        """
        total_sum = 0

        for val in data_values_list:
            total_sum += val
        if not data_values_list:
            return -1
        return total_sum / len(data_values_list)


class StatesMeanTask(Task):
    """
    Calculate mean of every state for a given question
    """

    def __init__(self, id, data, list_of_dict, used_as_helper_func=False):
        super().__init__(id, data, list_of_dict)
        self.used_as_helper_func = used_as_helper_func

    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:
            if dict_entry["Question"] == self.data["question"]:
                if dict_entry["LocationDesc"] in response_dict:
                    response_dict[dict_entry["LocationDesc"]].append(
                        float(dict_entry["Data_Value"])
                    )
                else:
                    response_dict[dict_entry["LocationDesc"]] = [
                        float(dict_entry["Data_Value"])
                    ]

        for state in response_dict:
            response_dict[state] = self.calculate_mean(response_dict[state])

            if response_dict[state] == -1:
                self.logger.error("(StatesMeanTask): State %s has no data.", state)

        # if it's not in best is min it's the other way
        if self.data["question"] in self.questions_best_is_min:
            response_dict = dict(
                sorted(response_dict.items(), key=lambda item: item[1])
            )
        else:
            response_dict = dict(
                sorted(response_dict.items(), key=lambda item: item[1], reverse=True)
            )

        return response_dict


class StateMeanTask(Task):
    """
    Calculate mean of a state for a given question
    """
    def solve(self):
        total_sum = 0
        total_count = 0

        for dict_entry in self.list_of_dict:
            if (
                dict_entry["Question"] == self.data["question"]
                and dict_entry["LocationDesc"] == self.data["state"]
            ):
                total_sum += float(dict_entry["Data_Value"])
                total_count += 1

        if total_count == 0:
            self.logger.error(
                "(StateMeanTask): The question and state given have no entries in the survey."
            )
            return {
                "error": "The question and state given have no entries in the survey"
            }

        mean = total_sum / total_count

        return {self.data["state"]: mean}


class BestFiveTask(Task):
    """
    Calculate the best five states for a given question
    """
    def solve(self):
        # self.logger.info("Started working on best five task job with id: %d.", self.id)
        response_dict = StatesMeanTask(
            self.id, self.data, self.list_of_dict, True
        ).solve()

        if len(list(response_dict.items())) < 5:
            self.logger.error(
                "(BestFiveTask): The given question has too few states which have participants that responded."
            )
            return {
                "error": "The given question has too few states which have participants that responded."
            }

        return dict(list(response_dict.items())[:5])


class WorstFiveTask(Task):
    """
    Calculate the worst five states for a given question
    """
    def solve(self):
        response_dict = StatesMeanTask(
            self.id, self.data, self.list_of_dict, True
        ).solve()

        if len(list(response_dict.items())) < 5:
            self.logger.error(
                "(WorstFiveTask): The given question has too few states which have participants that responded."
            )
            return {
                "error": "The given question has too few states which have participants that responded."
            }

        return dict(list(response_dict.items())[-5:])


class GlobalMeanTask(Task):
    """
        Calculte the global mean for a given question
    """
    def solve(self):
        total_sum = 0
        total_count = 0

        for dict_entry in self.list_of_dict:
            if dict_entry["Question"] == self.data["question"]:
                total_sum += float(dict_entry["Data_Value"])
                total_count += 1

        if total_count == 0:
            self.logger.error(
                "(GlobalMeanTask): Given question does not have enough responders."
            )
            return {"error": "Given question does not have enough responders."}

        mean = total_sum / total_count

        return {"global_mean": mean}


class DiffFromMeanTask(Task):
    """
    Calculate the difference from the global mean for a given question for each state
    """
    def solve(self):
        response_dict = {}
        global_resp_count = 0
        global_resp_sum = 0

        for dict_entry in self.list_of_dict:
            if dict_entry["Question"] == self.data["question"]:
                global_resp_count += 1
                global_resp_sum += float(dict_entry["Data_Value"])

                if dict_entry["LocationDesc"] in response_dict:
                    response_dict[dict_entry["LocationDesc"]].append(
                        float(dict_entry["Data_Value"])
                    )
                else:
                    response_dict[dict_entry["LocationDesc"]] = [
                        float(dict_entry["Data_Value"])
                    ]

        if global_resp_count == 0:
            self.logger.error(
                "(DiffFromMeanTask): Given question does not have enough responders."
            )
            return {"error": "Given question does not have enough responders."}

        for state in response_dict:
            response_dict[state] = (
                global_resp_sum / global_resp_count
            ) - self.calculate_mean(response_dict[state])

        return response_dict


class StateDiffFromMeanTask(Task):
    """
    Calculate the difference from the global mean for a given question for a given state
    """
    def solve(self):
        global_resp_count = 0
        global_resp_sum = 0

        state_sum = 0
        state_count = 0

        for dict_entry in self.list_of_dict:
            if dict_entry["Question"] == self.data["question"]:
                global_resp_count += 1
                global_resp_sum += float(dict_entry["Data_Value"])

                if dict_entry["LocationDesc"] == self.data["state"]:
                    state_count += 1
                    state_sum += float(dict_entry["Data_Value"])

        if global_resp_count == 0 or state_count == 0:
            self.logger.error(
                "(StateDiffFromMeanTask): Given question does not have enough responders."
            )
            return {"error": "Given question does not have enough responders."}

        res = (global_resp_sum / global_resp_count) - (state_sum / state_count)

        return {self.data["state"]: res}


class MeanByCategoryTask(Task):
    """
    Calculate the mean of a question for each category in a state for all the states
    """
    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:
            if dict_entry["Question"] != self.data["question"]:
                continue
            if (
                dict_entry["StratificationCategory1"]
                and dict_entry["LocationDesc"]
                and dict_entry["Stratification1"]
            ):
                tuple_string = str(
                    (
                        dict_entry["LocationDesc"],
                        dict_entry["StratificationCategory1"],
                        dict_entry["Stratification1"],
                    )
                )
                if tuple_string not in response_dict:
                    response_dict[tuple_string] = [float(dict_entry["Data_Value"])]
                else:
                    response_dict[tuple_string].append(float(dict_entry["Data_Value"]))

        for key in response_dict:
            response_dict[key] = self.calculate_mean(response_dict[key])

            if response_dict[key] == -1:
                self.logger.error("(MeanByCategoryTask): The key %s has no data.", key)

        return dict(sorted(response_dict.items()))


class StateMeanByCategoryTask(Task):
    """
    Calculate the mean of a question for each category in a state
    """
    def solve(self):
        response_dict = {}

        for dict_entry in self.list_of_dict:

            if (
                dict_entry["Question"] != self.data["question"]
                or dict_entry["LocationDesc"] != self.data["state"]
            ):
                continue

            if dict_entry["StratificationCategory1"] and dict_entry["Stratification1"]:
                tuple_string = str(
                    (
                        dict_entry["StratificationCategory1"],
                        dict_entry["Stratification1"],
                    )
                )
                if tuple_string not in response_dict:
                    response_dict[tuple_string] = [float(dict_entry["Data_Value"])]
                else:
                    response_dict[tuple_string].append(float(dict_entry["Data_Value"]))

        for key in response_dict:
            response_dict[key] = self.calculate_mean(response_dict[key])

            if response_dict[key] == -1:
                self.logger.error(
                    "(StateMeanByCategoryTask): The key %s has no data.", key
                )

        response_dict = dict(sorted(response_dict.items()))

        return {self.data["state"]: response_dict}
