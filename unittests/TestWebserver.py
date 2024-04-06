"""
    Module for testing the web server by generating requests like the checker.
    Inspired from the checker.
    This class must be run from the root directory of the project.
    python3 -m unittest unittests/TestWebserver.py
"""

import unittest
import json
import requests
from deepdiff import DeepDiff


# This class can be run from its directory
class TestWebServer(unittest.TestCase):
    """
    Class implementation for testing the web server.
    """

    # unit test for a states mean
    def test_states_mean(self):
        """
        Test method for StatesMeanTask.
        """
        req_data = None

        with open("unittests/inputs/in_states_mean.txt", "r", encoding="utf-8") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_states_mean): Could not load input")
            return
        res = requests.post(
            "http://127.0.0.1:5000/api/states_mean", json=req_data, timeout=0.2
        )
        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
        # Asserting the response data
        response_data = res.json()
        job_id = response_data["job_id"]

        res = requests.get(
            f"http://127.0.0.1:5000/api/get_results/{job_id}", timeout=0.2
        )

        response_data = res.json()

        ref_data = None

        with open("unittests/refs/ref_states_mean.txt", "r", encoding="utf-8") as fin:
            ref_data = json.load(fin)

        if not ref_data:
            print("(test_states_mean): Could not load refs")
            return

        d = DeepDiff(response_data["data"], ref_data, math_epsilon=0.01)

        self.assertTrue(d == {}, str(d))

    def test_state_mean_by_category(self):
        """
        Test method for StateMeanByCategoryTask.
        """
        req_data = None

        with open("unittests/inputs/in_state_mean_by_category.txt", "r", encoding="utf-8") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_state_mean_by_category): Could not load input")
            return

        res = requests.post(
            "http://127.0.0.1:5000/api/state_mean_by_category",
            json=req_data,
            timeout=0.2,
        )
        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
        # Asserting the response data
        response_data = res.json()
        job_id = response_data["job_id"]
        res = requests.get(
            f"http://127.0.0.1:5000/api/get_results/{job_id}", timeout=0.2
        )
        response_data = res.json()

        ref_data = None

        with open("unittests/refs/ref_state_mean_by_category.txt", "r", encoding="utf-8") as fin:
            ref_data = json.load(fin)

        if not ref_data:
            print("(test_states_mean): Could not load refs")
            return

        d = DeepDiff(response_data["data"], ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_state_diff_from_mean(self):
        """
        Test method for StateDiffFromMeanTask.
        """
        req_data = None

        with open("unittests/inputs/in_state_diff_from_mean.txt", "r", encoding="utf-8") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_state_diff_from_mean): Could not load input")
            return

        res = requests.post(
            "http://127.0.0.1:5000/api/state_diff_from_mean", json=req_data, timeout=0.2
        )

        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)

        # Asserting the response data
        response_data = res.json()

        job_id = response_data["job_id"]

        res = requests.get(
            f"http://127.0.0.1:5000/api/get_results/{job_id}", timeout=0.2
        )

        response_data = res.json()

        ref_data = None

        with open("unittests/refs/ref_state_diff_from_mean.txt", "r", encoding="utf-8") as fin:
            ref_data = json.load(fin)

        if not ref_data:
            print("(test_state_diff_from_mean): Could not load refs")
            return

        d = DeepDiff(response_data["data"], ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_get_results_invalid_job_id(self):
        """
        Test method for get_results with invalid job_id.
        """
        res = requests.get("http://127.0.0.1:5000/api/get_results/1000", timeout=0.2)
        response_data = res.json()

        self.assertTrue(response_data["status"], "error")
        self.assertTrue(response_data["reason"], "Invalid job_id")

    def test_y_submit_task_after_graceful_shutdown(self):
        """
        Test method for submitting a task after graceful shutdown.
        """
        res = requests.get("http://127.0.0.1:5000/api/graceful_shutdown", timeout=0.2)
        response_data = res.json()

        self.assertTrue(response_data["status"], "done")
        self.assertTrue(response_data["data"], "Server closed!")

        # now try to submit a new task
        req_data = None

        with open("unittests/inputs/in_state_diff_from_mean.txt", "r", encoding="utf-8") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_state_diff_from_mean): Could not load input")
            return

        res = requests.post(
            "http://127.0.0.1:5000/api/state_diff_from_mean", json=req_data, timeout=0.2
        )
        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
        # Asserting the response data
        response_data = res.json()
        self.assertTrue(response_data["Failed"], "Server is closed")

    # there must be 0 jobs that remained unprocessed after graceful shutdown
    def test_y_num_jobs_after_graceful_shutdown(self):
        """
        Test method for getting the number of unsolved jobs after graceful shutdown.
        """
        res = requests.get("http://127.0.0.1:5000/api/graceful_shutdown", timeout=0.2)
        response_data = res.json()

        self.assertTrue(response_data["status"], "done")
        self.assertTrue(response_data["data"], "Server closed!")

        res = requests.get("http://127.0.0.1:5000/api/num_jobs", timeout=0.2)
        response_data = res.json()

        self.assertTrue(response_data["status"], "done")

        # equal not true
        self.assertEqual(response_data["data"], 0)

    # all should be finished after graceful shutdown
    def test_y_jobs_after_graceful_shutdown(self):
        """
        Test method for getting the status of all jobs after graceful shutdown.
        """
        res = requests.get("http://127.0.0.1:5000/api/graceful_shutdown", timeout=0.2)
        response_data = res.json()

        self.assertTrue(response_data["status"], "done")
        self.assertTrue(response_data["data"], "Server closed!")

        res = requests.get("http://127.0.0.1:5000/api/jobs", timeout=0.2)
        response_data = res.json()
        self.assertTrue(response_data["status"], "done")

        data_dict_list = response_data["data"]

        job_id = 1

        for data_dict in data_dict_list:
            self.assertTrue(data_dict[f"job_id_{job_id}"], "done")
            job_id += 1

    def test_z_graceful_shutdown(self):
        """
        Test method for checking if the server is closed after graceful shutdown.
        """
        res = requests.get("http://127.0.0.1:5000/api/graceful_shutdown", timeout=0.2)
        response_data = res.json()

        self.assertTrue(response_data["status"], "done")
        self.assertTrue(response_data["data"], "Server closed!")
