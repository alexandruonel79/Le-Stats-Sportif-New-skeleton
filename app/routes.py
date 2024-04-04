from app import webserver
from flask import request, jsonify

import os
import json
import logging

# posibil nu e bn
from app.Task import *
from app.task_runner import ThreadPool
from app import jobs_states_func

# Example endpoint definition
@webserver.route("/api/post_endpoint", methods=["POST"])
def post_endpoint():
    if request.method == "POST":
        # Assuming the request contains JSON data
        data = request.json
        #print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405


@webserver.route("/api/get_results/<job_id>", methods=["GET"])
def get_response(job_id):
    #print(f"JobID is {job_id}")
    job_id = int(job_id)
    # TODO
    webserver.logger.info("Requested solution for job_%d.", job_id)
    # Check if job_id is valid
    #print(f"Current counter is {webserver.job_counter} and job_id is {job_id}")
    if webserver.job_counter <= job_id or job_id <= 0:
        webserver.logger.error("Server received request for an invalid job id: %d.", job_id)
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })
    res = jobs_states_func.get_result_by_Id(job_id, webserver.tasks_runner.get_fs_lock())
    webserver.logger.info("Received solution for job_%d.", job_id)
    # If not, return running status
    return jsonify(res)




@webserver.route("/api/jobs", methods=["GET"])
def get_all_jobs_status():
    webserver.logger.info("Requested all jobs status.")
    res = jobs_states_func.get_all_jobs_status_func(webserver.job_counter, webserver.tasks_runner.get_fs_lock())
    # response_dict = {}
    # response_dict["status"] = "done"
    # response_dict["data"] = res
    #print({"status": "done", "data": res})
    webserver.logger.info("Received all jobs status.")
    return jsonify({"status": "done", "data": res})

@webserver.route("/api/states_mean", methods=["POST"])
def states_mean_request():
    # Get request data
    data = request.json
    webserver.logger.info("(/api/states_mean): Request body: %s.", data)
    #print(f"Got request {data}")

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    registered = webserver.tasks_runner.submitTask(
        StatesMeanTask(webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict())
    )

    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    
    webserver.job_counter += 1

    webserver.logger.info("Registered job states mean with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


# acum test
@webserver.route("/api/graceful_shutdown", methods=["GET"])
def graceful_shutdown():
    print("Closing server")
    webserver.logger.info("(/api/graceful_shutdown): Requested server shutdown.")
    webserver.tasks_runner.stop()
    webserver.logger.info("(/api/graceful_shutdown): Server closed the threadpool.")
    print("Server closed")
    webserver.tasks_runner.check_threads()
    return jsonify({"status": "done", "data": "Server closed!"})


# acum test
@webserver.route("/api/num_jobs", methods=["GET"])
def num_jobs():
    webserver.logger.info("(/api/num_jobs): Requested number of jobs that are still waiting.")
    res = jobs_states_func.get_unsolved_jobs_count(webserver.job_counter, webserver.tasks_runner.get_fs_lock())
    webserver.logger.info("(/api/num_jobs): Received a total of %d unsolved jobs.", res)
    return jsonify({"status": "done", "data": res})

@webserver.route("/api/state_mean", methods=["POST"])
def state_mean_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/state_mean): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        StateMeanTask(webserver.job_counter, data,  webserver.data_ingestor.get_list_of_dict())
    )
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/state_mean): Registered job state mean with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route("/api/best5", methods=["POST"])
def best5_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/best5): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        BestFiveTask(webserver.job_counter, data,  webserver.data_ingestor.get_list_of_dict())
    )

    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})  
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/best5): Registered job best five with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/worst5", methods=["POST"])
def worst5_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/worst5): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        WorstFiveTask(webserver.job_counter, data,  webserver.data_ingestor.get_list_of_dict())
    )

    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/worst5): Registered job worst five with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/global_mean", methods=["POST"])
def global_mean_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/global_mean): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        GlobalMeanTask(webserver.job_counter, data,  webserver.data_ingestor.get_list_of_dict())
    )
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/global_mean): Registered job global mean with id %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/diff_from_mean", methods=["POST"])
def diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/diff_from_mean): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        DiffFromMeanTask(webserver.job_counter, data,  webserver.data_ingestor.get_list_of_dict())
    )

    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/diff_from_mean): Registered job diff from mean with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/state_diff_from_mean", methods=["POST"])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/state_diff_from_mean): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        StateDiffFromMeanTask(webserver.job_counter, data,  webserver.data_ingestor.get_list_of_dict())
    )
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/state_diff_from_mean): Registered job state diff from mean with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/mean_by_category", methods=["POST"])
def mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/mean_by_category): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        MeanByCategoryTask(webserver.job_counter, data,  webserver.data_ingestor.get_list_of_dict())
    )
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/mean_by_category): Registered job mean by category with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/state_mean_by_category", methods=["POST"])
def state_mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    webserver.logger.info("(/api/state_mean_by_category): Request body: %s.", data)
    #print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    registered = webserver.tasks_runner.submitTask(
        StateMeanByCategoryTask(webserver.job_counter, data, webserver.data_ingestor.get_list_of_dict())
    )
    if not registered:
        webserver.logger.error("Server received request but it's closed")
        return jsonify({"Failed": "Server is closed"})
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    webserver.logger.info("(/api/state_mean_by_category): Registered job state mean by category with id: %d.", webserver.job_counter - 1)
    return jsonify({"job_id": webserver.job_counter - 1})


# You can check localhost in your browser to see what this displays
@webserver.route("/")
@webserver.route("/index")
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ", ".join(rule.methods)
        routes.append(f'Endpoint: "{rule}" Methods: "{methods}"')
    return routes
