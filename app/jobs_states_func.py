"""
    Module for getting the job status.
    General idea: Checking if a job is ready or still running
    is done by checking the existence of the file
    if the file does not exist, it is still running
"""

import os
import json


def get_result_by_id(job_id: int) -> dict:
    """
    Returns: a dictionary with the status of the job
    """
    file_path = "results/job_id_" + str(job_id) + ".txt"

    try:
        with open(file_path, "r", encoding='utf-8') as file:
            result = json.load(file)
            return {"status": "done", "data": result}
    except (json.JSONDecodeError, FileNotFoundError):
        return {"status": "running"}


def get_all_jobs_status_func(last_job_id: int) -> list:
    """
    Returns: list of dictionaries with the status of the jobs
    """
    data_list = []
    for i in range(1, last_job_id):
        file_path = "results/job_id_" + str(i) + ".txt"

        if os.path.exists(file_path):
            data_list.append({f"job_id_{i}": "done"})
        else:
            data_list.append({f"job_id_{i}": "running"})

    return data_list


def get_unsolved_jobs_count(last_job_id: int) -> int:
    """
    Returns: the number of unsolved jobs
    """
    unsolved = 0

    for i in range(1, last_job_id):
        file_path = "results/job_id_" + str(i) + ".txt"
        if not os.path.exists(file_path):
            unsolved += 1

    return unsolved
