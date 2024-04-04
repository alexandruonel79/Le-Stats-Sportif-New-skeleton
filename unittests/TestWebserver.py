import unittest
import os
import json
import requests
from deepdiff import DeepDiff
import time 

# https://stackoverflow.com/questions/4095319/unittest-tests-order
# unittest.defaultTestLoader.sortTestMethodsUsing = lambda *args: -1

class TestWebServer(unittest.TestCase):
    # unit test for a states mean
    def test_states_mean(self):
        req_data = None

        with open(f"inputs/in_states_mean.txt", "r") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_states_mean): Could not load input")
            return
        
        res = requests.post("http://127.0.0.1:5000/api/states_mean", json=req_data)

        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
    
        # Asserting the response data
        response_data = res.json()
        
        job_id = response_data["job_id"]
        #time.sleep(0.2)
        res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")

        response_data = res.json()
        # with open("test_Debug.json", "w") as json_file:
        #     # Serialize the data and write it to the file
        #     json.dump(response_data, json_file)
        ref_data = None

        with open("refs/ref_states_mean.txt", "r") as fin:
            ref_data = json.load(fin)

        if not ref_data:
            print("(test_states_mean): Could not load refs")
            return
        
        d = DeepDiff(response_data['data'], ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))


    def test_state_mean_by_category(self):
        req_data = None

        with open(f"inputs/in_state_mean_by_category.txt", "r") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_state_mean_by_category): Could not load input")
            return
        
        res = requests.post("http://127.0.0.1:5000/api/state_mean_by_category", json=req_data)

        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
    
        # Asserting the response data
        response_data = res.json()
        
        job_id = response_data["job_id"]
        #time.sleep(0.2)
        res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")

        response_data = res.json()

        ref_data = None

        with open("refs/ref_state_mean_by_category.txt", "r") as fin:
            ref_data = json.load(fin)

        if not ref_data:
            print("(test_states_mean): Could not load refs")
            return
        
        d = DeepDiff(response_data['data'], ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_state_diff_from_mean(self):
        req_data = None

        with open(f"inputs/in_state_diff_from_mean.txt", "r") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_state_diff_from_mean): Could not load input")
            return
        
        res = requests.post("http://127.0.0.1:5000/api/state_diff_from_mean", json=req_data)

        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
    
        # Asserting the response data
        response_data = res.json()

        job_id = response_data["job_id"]
        print(f"Job id is {job_id}")
        #time.sleep(0.2)
        res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")

        response_data = res.json()
        # print(response_data)
        ref_data = None

        with open("refs/ref_state_diff_from_mean.txt", "r") as fin:
            ref_data = json.load(fin)

        if not ref_data:
            print("(test_state_diff_from_mean): Could not load refs")
            return
        
        d = DeepDiff(response_data['data'], ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_get_results_invalid_job_id(self):
        res = requests.get(f"http://127.0.0.1:5000/api/get_results/1000")
        response_data = res.json()
        # print(response_data)
        self.assertTrue(response_data['status'], "error" )
        self.assertTrue(response_data['reason'], "Invalid job_id")
    
    def test_y_submitTask_after_graceful_shutdown(self):
        res = requests.get(f"http://127.0.0.1:5000/api/graceful_shutdown")
        response_data = res.json()
        # print(response_data)
        self.assertTrue(response_data['status'], "done" )
        self.assertTrue(response_data['data'], "Server closed!")

        # now try to submit a new task
        req_data = None

        with open(f"inputs/in_state_diff_from_mean.txt", "r") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("(test_state_diff_from_mean): Could not load input")
            return
        
        res = requests.post("http://127.0.0.1:5000/api/state_diff_from_mean", json=req_data)

        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
    
        # Asserting the response data
        response_data = res.json()

        self.assertTrue(response_data['Failed'], "Server is closed")

    # there must be 0 jobs that remained unprocessed after graceful shutdown
    def test_y_num_jobs_after_graceful_shutdown(self):
        res = requests.get(f"http://127.0.0.1:5000/api/graceful_shutdown")
        response_data = res.json()
        # print(response_data)
        self.assertTrue(response_data['status'], "done" )
        self.assertTrue(response_data['data'], "Server closed!")

        res = requests.get("http://127.0.0.1:5000/api/num_jobs")
        response_data = res.json()
        print(response_data)
        self.assertTrue(response_data['status'], "done" )
        print(f"resp data: {type(response_data['data'])}")
        # equal not true
        self.assertEqual(response_data['data'], 0)

    # all should be finished after graceful shutdown
    def test_y_jobs_after_graceful_shutdown(self):
        res = requests.get(f"http://127.0.0.1:5000/api/graceful_shutdown")
        response_data = res.json()
        # print(response_data)
        self.assertTrue(response_data['status'], "done" )
        self.assertTrue(response_data['data'], "Server closed!")

        res = requests.get("http://127.0.0.1:5000/api/jobs")
        response_data = res.json()
        self.assertTrue(response_data['status'], "done" )
        
        data_dict_list = response_data['data']

        job_id = 1

        for data_dict in data_dict_list:
            self.assertTrue(data_dict[f"job_id_{job_id}"], "done")
            job_id += 1

    def test_z_graceful_shutdown(self):
        res = requests.get(f"http://127.0.0.1:5000/api/graceful_shutdown")
        response_data = res.json()
        print(response_data)
        self.assertTrue(response_data['status'], "done" )
        self.assertTrue(response_data['data'], "Server closed!")

# class Shutdown(unittest.TestCase):
#     def test_graceful_shutdown(self):
#         res = requests.get(f"http://127.0.0.1:5000/api/graceful_shutdown")
#         response_data = res.json()
#         print(response_data)
#         self.assertTrue(response_data['status'], "done" )
#         self.assertTrue(response_data['data'], "Server closed!")

# if __name__ == '__main__':
#     # run tests, first the basic ones then the shutdown
#     suite = unittest.TestSuite()
#     suite.addTest(BasicTests('test_states_mean'))
#     suite.addTest(BasicTests('test_state_mean_by_category'))
#     suite.addTest(BasicTests('test_state_diff_from_mean'))
#     suite.addTest(BasicTests('test_get_results_invalid_job_id'))
#     suite.addTest(Shutdown('test_graceful_shutdown'))
#     runner = unittest.TextTestRunner()

    # def test_graceful_shutdown(self):
    #     res = requests.get(f"http://127.0.0.1:5000/api/graceful_shutdown")
    #     response_data = res.json()
    #     print(response_data)
    #     self.assertTrue(response_data['status'], "done" )
    #     self.assertTrue(response_data['data'], "Server closed!")