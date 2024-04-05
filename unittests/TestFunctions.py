"""
   Module to test my functions without starting the server.
   This class must be run from the root directory of the project.
"""

import unittest
import json
from deepdiff import DeepDiff

from app.Task import (
    StatesMeanTask,
    StateMeanByCategoryTask,
    StateDiffFromMeanTask,
    StateMeanTask,
    BestFiveTask,
    WorstFiveTask,
    GlobalMeanTask,
    DiffFromMeanTask,
    MeanByCategoryTask,
)
from app.data_ingestor import DataIngestor

class TestFunctions(unittest.TestCase):
    """
    Class implementation for testing my own functions without starting the server.
    """

    # setup method
    def setUp(self):
        self.list_of_dict = DataIngestor(
            "nutrition_activity_obesity_usa_subset.csv"
        ).get_list_of_dict()

    def test_states_mean_task(self):
        """
        Test method for StateMeanTask.
        """
        with open("unittests/inputs/in_states_mean.txt", encoding="utf-8") as f:
            data = json.load(f)

        with open("unittests/refs/ref_states_mean.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = StatesMeanTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_state_mean_by_category(self):
        """
        Test method for StateMeanByCategoryTask.
        """
        with open(
            "unittests/inputs/in_state_mean_by_category.txt", encoding="utf-8"
        ) as f:
            data = json.load(f)

        with open(
            "unittests/refs/ref_state_mean_by_category.txt", encoding="utf-8"
        ) as f:
            ref_data = json.load(f)

        task = StateMeanByCategoryTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_state_diff_from_mean(self):
        """
        Test method for StateDiffFromMeanTask.
        """
        with open(
            "unittests/inputs/in_state_diff_from_mean.txt", encoding="utf-8"
        ) as f:
            data = json.load(f)

        with open("unittests/refs/ref_state_diff_from_mean.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = StateDiffFromMeanTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_state_mean(self):
        """
        Test method for StateMeanTask.
        """
        with open("unittests/inputs/in_state_mean.txt", encoding="utf-8") as f:
            data = json.load(f)

        with open("unittests/refs/ref_state_mean.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = StateMeanTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_best_five(self):
        """
        Test method for BestFiveTask.
        """
        with open("unittests/inputs/in_best_five.txt", encoding="utf-8") as f:
            data = json.load(f)

        with open("unittests/refs/ref_best_five.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = BestFiveTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_worst_five(self):
        """
        Test method for WorstFiveTask.
        """
        with open("unittests/inputs/in_worst_five.txt", encoding="utf-8") as f:
            data = json.load(f)

        with open("unittests/refs/ref_worst_five.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = WorstFiveTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_global_mean(self):
        """
        Test method for GlobalMeanTask.
        """
        with open("unittests/inputs/in_global_mean.txt", encoding="utf-8") as f:
            data = json.load(f)

        with open("unittests/refs/ref_global_mean.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = GlobalMeanTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_diff_from_mean(self):
        """
        Test method for DiffFromMeanTask.
        """
        with open("unittests/inputs/in_diff_from_mean.txt", encoding="utf-8") as f:
            data = json.load(f)

        with open("unittests/refs/ref_diff_from_mean.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = DiffFromMeanTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_mean_by_category(self):
        """
        Test method for MeanByCategoryTask.
        """
        with open("unittests/inputs/in_mean_by_category.txt", encoding="utf-8") as f:
            data = json.load(f)

        with open("unittests/refs/ref_mean_by_category.txt", encoding="utf-8") as f:
            ref_data = json.load(f)

        task = MeanByCategoryTask(1, data, self.list_of_dict)
        # solve it
        task_res = task.solve()
        # check if task_res is correct
        d = DeepDiff(task_res, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
