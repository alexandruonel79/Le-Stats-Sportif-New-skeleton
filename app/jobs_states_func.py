import os
import json
from threading import Lock

def get_result_by_Id(job_id: int, lock: Lock) -> list:
    file_path = "results/job_id_" + str(job_id) + ".txt"
    with lock:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                result = json.load(file)
                return {"status": "done", "data": result}
        else:
            return {"status": "running"}

def get_all_jobs_status_func(last_job_id: int, lock: Lock) -> dict:
    data_list = []
    
    for i in range(1, last_job_id):
        file_path = "results/job_id_" + str(i) + ".txt"
        with lock:
            if os.path.exists(file_path):
                data_list.append({f"job_id_{i}": "done"})
            else:
                data_list.append({f"job_id_{i}": "running"})
    
    return data_list

def get_unsolved_jobs_count(last_job_id: int, lock: Lock) -> int:
    unsolved = 0

    for i in range(1, last_job_id):
        file_path = "results/job_id_" + str(i) + ".txt"
        with lock:
            if not os.path.exists(file_path):
                unsolved += 1
                
    return unsolved
