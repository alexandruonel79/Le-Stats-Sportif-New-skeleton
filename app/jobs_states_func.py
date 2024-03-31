import os
import json

def get_result_by_Id(job_id: int) -> list:
    file_path = "results/job_id_" + str(job_id) + ".txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            result = json.load(file)
            return {"status": "done", "data": result}
    else:
        return {"status": "running"}

def get_all_jobs_status_func(last_job_id: int) -> dict:
    data_list = []
    
    for i in range(1, last_job_id):
        file_path = "results/job_id_" + str(i) + ".txt"
        if os.path.exists(file_path):
            data_list.append({f"job_id_{i}": "done"})
        else:
            data_list.append({f"job_id_{i}": "running"})
    
    return data_list
