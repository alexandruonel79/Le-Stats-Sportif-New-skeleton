"""
    Module for all the routes of the application. It registers the jobs
    and returns the results when they are requested and ready.
"""

from flask import request, jsonify
from app import webserver
from app.Task import (
    StatesMeanTask,
    StateMeanTask,
    BestFiveTask,
    WorstFiveTask,
    GlobalMeanTask,
    DiffFromMeanTask,
    StateDiffFromMeanTask,
    MeanByCategoryTask,
    StateMeanByCategoryTask,
)
from app import jobs_states_func


@webserver.route("/api/get_results/<job_id>", methods=["GET"])
def get_response(job_id):
    """
    Checks if the job id is valid, and if it is, returns the result of the job.
    """
    job_id = int(job_id)
    webserver.logger.info(
        "(/api/get_results/%d): Requested solution for job_%d.", job_id, job_id
    )
    # check if the job_id is valid
    if webserver.job_counter <= job_id or job_id <= 0:
        webserver.logger.error(
            "Server received request for an invalid job id: %d.", job_id
        )
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    # get the result
    res = jobs_states_func.get_result_by_id(job_id)
    webserver.logger.info(
        "(/api/get_results/%d): Received solution for job_%d.", job_id, job_id
    )
    return jsonify(res)


@webserver.route("/api/jobs", methods=["GET"])
def get_all_jobs_status():
    """
    Checks all the jobs status and returns them.
    """
    webserver.logger.info("(/api/jobs): Requested all jobs status.")
    res = jobs_states_func.get_all_jobs_status_func(webserver.job_counter)
    webserver.logger.info("Received all jobs status.")
    return jsonify({"status": "done", "data": res})


@webserver.route("/api/states_mean", methods=["POST"])
def states_mean_request():
    """
    Registers a job for the states mean task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/states_mean): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        StatesMeanTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})

    # increment the job counter
    webserver.job_counter += 1

    webserver.logger.info(
        "Registered job states mean with id: %d.", webserver.job_counter - 1
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/graceful_shutdown", methods=["GET"])
def graceful_shutdown():
    """
    Closes the server gracefully, meaning it will wait for all the jobs to finish.
    """
    webserver.logger.info("(/api/graceful_shutdown): Requested server shutdown.")
    webserver.tasks_runner.stop()
    webserver.logger.info("(/api/graceful_shutdown): Server closed the threadpool.")
    return jsonify({"status": "done", "data": "Server closed!"})


@webserver.route("/api/num_jobs", methods=["GET"])
def num_jobs():
    """
    Gets the number of jobs that are still waiting to be solved.
    """
    webserver.logger.info(
        "(/api/num_jobs): Requested number of jobs that are still waiting."
    )
    res = jobs_states_func.get_unsolved_jobs_count(webserver.job_counter)
    webserver.logger.info("(/api/num_jobs): Received a total of %d unsolved jobs.", res)
    return jsonify({"status": "done", "data": res})


@webserver.route("/api/state_mean", methods=["POST"])
def state_mean_request():
    """
    Registers a job for the state mean task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/state_mean): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        StateMeanTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    webserver.logger.info(
        "(/api/state_mean): Registered job state mean with id: %d.",
        webserver.job_counter - 1,
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/best5", methods=["POST"])
def best5_request():
    """
    Registers a job for the best five task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/best5): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        BestFiveTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    webserver.logger.info(
        "(/api/best5): Registered job best five with id: %d.", webserver.job_counter - 1
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/worst5", methods=["POST"])
def worst5_request():
    """
    Registers a job for the worst five task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/worst5): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        WorstFiveTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    webserver.logger.info(
        "(/api/worst5): Registered job worst five with id: %d.",
        webserver.job_counter - 1,
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/global_mean", methods=["POST"])
def global_mean_request():
    """
    Registers a job for the global mean task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/global_mean): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        GlobalMeanTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    webserver.logger.info(
        "(/api/global_mean): Registered job global mean with id %d.",
        webserver.job_counter - 1,
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/diff_from_mean", methods=["POST"])
def diff_from_mean_request():
    """
    Registers a job for the diff from mean task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/diff_from_mean): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        DiffFromMeanTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    webserver.logger.info(
        "(/api/diff_from_mean): Registered job diff from mean with id: %d.",
        webserver.job_counter - 1,
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/state_diff_from_mean", methods=["POST"])
def state_diff_from_mean_request():
    """
    Registers a job for the state diff from mean task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/state_diff_from_mean): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        StateDiffFromMeanTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    webserver.logger.info(
        "(/api/state_diff_from_mean): Registered job state diff from mean with id: %d.",
        webserver.job_counter - 1,
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/mean_by_category", methods=["POST"])
def mean_by_category_request():
    """
    Registers a job for the mean by category task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/mean_by_category): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        MeanByCategoryTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    webserver.logger.info(
        "(/api/mean_by_category): Registered job mean by category with id: %d.",
        webserver.job_counter - 1,
    )
    # Return associated job_id
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/state_mean_by_category", methods=["POST"])
def state_mean_by_category_request():
    """
    Registers a job for the state mean by category task.
    """
    # Get request data
    data = request.json
    webserver.logger.info("(/api/state_mean_by_category): Request body: %s.", data)
    # register the job
    registered = webserver.tasks_runner.submit_task(
        StateMeanByCategoryTask(
            webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict()
        )
    )
    # if the job it's not registered, send an error
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # increment the job counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info(
        "(/api/state_mean_by_category): Registered job state mean by category with id: %d.",
        webserver.job_counter - 1,
    )
    return jsonify({"job_id": webserver.job_counter - 1})


def get_defined_routes():
    """
    Sets all the routes.
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ", ".join(rule.methods)
        routes.append(f'Endpoint: "{rule}" Methods: "{methods}"')
    return routes
