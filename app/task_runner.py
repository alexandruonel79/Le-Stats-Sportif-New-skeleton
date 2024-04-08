"""
    Module that contains the custom ThreadPool, which manages all the jobs
"""

import os
import json

from queue import Queue
from threading import Thread, Event, Lock
from app.Task import Task


class ThreadPool:
    """
    Custom ThreadPool implementation
    """

    def __init__(self):
        # check if an environment variable 'TP_NUM_OF_THREADS' is defined
        # if it is, then that is the number of threads to be used
        if "TP_NUM_OF_THREADS" in os.environ:
            self.num_of_threads = int(os.environ["TP_NUM_OF_THREADS"])
        else:
            self.num_of_threads = os.cpu_count()
        # the job queue
        self.task_queue = Queue()
        # the event is triggered in routes when the graceful shutdown is called
        self.shutdown_event = Event()
        # holds all the taskRunner threads
        self.threads_list = []
        # lock used for letting just one thread acces the queue and the event
        self.lock = Lock()
        # event for when a new job is submitted
        self.new_job_event = Event()

    def start(self):
        """
        Creates all the TaskRunner threads and starts them
        """
        for i in range(self.num_of_threads):
            self.threads_list.append(
                TaskRunner(
                    self.shutdown_event, self.task_queue, self.lock, self.new_job_event
                )
            )
            self.threads_list[i].start()

    def stop(self):
        """
        Gracefully shutdown all the threads, meaning they stop after
        the queue is empty and all the tasks are done
        """
        # signal the threads so they pass the wait()
        self.new_job_event.set()
        # set the shutdown event on
        self.shutdown_event.set()
        # join the threads
        for thread in self.threads_list:
            thread.join()

    def submit_task(self, task: Task) -> bool:
        """
        Adds a task in the queue.
        Returns: True if the task was added, False if the ThreadPool is shutting down.
        """
        # if the shutdown event is not set
        # use the lock to access the queue and the event
        if not self.shutdown_event.is_set():
            with self.lock:
                self.task_queue.put(task)
                self.new_job_event.set()
            return True
        else:
            return False


class TaskRunner(Thread):
    """
    Custom TaskRunner implementation
    """

    def __init__(
        self, shutdown_event: Event, task_queue: Queue, lock: Lock, new_job_event: Event
    ):
        super().__init__()
        # set the internal variables
        self.shutdown_event = shutdown_event
        self.task_queue = task_queue
        self.lock = lock
        self.new_job_event = new_job_event

    def save_result(self, result, task_id):
        """
        Saves the result as a json to disk
        """
        with open(f"results/job_id_{task_id}.txt", "w", encoding="utf-8") as f:
            json.dump(result, f)

    def run(self):
        # if all the jobs are done and shutdown event is set
        # then the thread can finish
        while not (self.shutdown_event.is_set() and self.task_queue.empty()):
            # wait until the event is set
            self.new_job_event.wait()

            with self.lock:
                if self.task_queue.empty():
                    # clear the signal and let the threads wait for the next job
                    self.new_job_event.clear()
                    continue
                # otherwise get the job
                task = self.task_queue.get()
            # solve the job and save the result
            result = task.solve()
            self.save_result(result, task.id)
