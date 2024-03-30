from app import webserver
from flask import request, jsonify

import os
import json

# posibil nu e bn
from app.Task import *
from app.task_runner import ThreadPool

# Example endpoint definition
@webserver.route("/api/post_endpoint", methods=["POST"])
def post_endpoint():
    if request.method == "POST":
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

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
    print(f"JobID is {job_id}")
    job_id = int(job_id)
    # TODO
    # Check if job_id is valid
    #print(f"Current counter is {webserver.job_counter} and job_id is {job_id}")
    if webserver.job_counter <= job_id:
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })
    res = webserver.tasks_runner.get_job_state(job_id)
    # If not, return running status
    return jsonify(res)




@webserver.route("/api/jobs", methods=["GET"])
def get_all_jobs_status():
    res = webserver.tasks_runner.get_all_jobs_states()
    # response_dict = {}
    # response_dict["status"] = "done"
    # response_dict["data"] = res
    print({"status": "done", "data": res})
    return jsonify({"status": "done", "data": res})

@webserver.route("/api/states_mean", methods=["POST"])
def states_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data}")

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    webserver.tasks_runner.submitTask(
        StatesMeanTask(webserver.job_counter, data, webserver)
    )
    webserver.job_counter += 1

    return jsonify({"job_id": webserver.job_counter - 1})


# acum test
@webserver.route("/api/graceful_shutdown", methods=["GET"])
def ceva():
    print("Closing server")
    webserver.tasks_runner.stop()
    print("Server closed")
    webserver.tasks_runner.check_threads()
    return jsonify({"status": "NotImplemented"})


@webserver.route("/api/state_mean", methods=["POST"])
def state_mean_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        StateMeanTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route("/api/best5", methods=["POST"])
def best5_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        BestFiveTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/worst5", methods=["POST"])
def worst5_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        WorstFiveTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/global_mean", methods=["POST"])
def global_mean_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        GlobalMeanTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/diff_from_mean", methods=["POST"])
def diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        DiffFromMeanTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/state_diff_from_mean", methods=["POST"])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        StateDiffFromMeanTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/mean_by_category", methods=["POST"])
def mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        MeanByCategoryTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route("/api/state_mean_by_category", methods=["POST"])
def state_mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    print(f"Got request {data}")
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.submitTask(
        StateMeanByCategoryTask(webserver.job_counter, data, webserver)
    )
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

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
