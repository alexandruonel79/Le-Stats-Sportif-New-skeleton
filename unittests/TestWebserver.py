import unittest
import os
import json
import requests
from deepdiff import DeepDiff

class TestWebserver(unittest.TestCase):

    def test_states_mean(self):
        req_data = None

        with open(f"inputs/in_states_mean.txt", "r") as fin:
            req_data = json.load(fin)

        if not req_data:
            print("Could not load input")
            return
        
        res = requests.post("http://127.0.0.1:5000/api/states_mean", json=req_data)

        # Asserting that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
    
        # Asserting the response data
        response_data = res.json()
        
        job_id = response_data["job_id"]

        res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")

        response_data = res.json()
        # with open("test_Debug.json", "w") as json_file:
        #     # Serialize the data and write it to the file
        #     json.dump(response_data, json_file)
        ref_data = None

        with open("refs/out_states_mean.txt", "r") as fin:
            ref_data = json.load(fin)

        d = DeepDiff(response_data['data'], ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
