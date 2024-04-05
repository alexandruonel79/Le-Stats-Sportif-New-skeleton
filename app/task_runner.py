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
        # check if an environment variable TP_NUM_OF_THREADS is defined
        if "TP_NUM_OF_THREADS" in os.environ:
            self.num_of_threads = int(os.environ["TP_NUM_OF_THREADS"])
        else:
            self.num_of_threads = os.cpu_count()

        self.task_queue = Queue()
        self.shutdown_event = Event()
        self.threads_list = []
        self.lock = Lock()
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
        self.new_job_event.set()
        self.shutdown_event.set()
        for thread in self.threads_list:
            thread.join()

    def submit_task(self, task: Task) -> bool:
        """
        Adds a task in the queue.
        Returns: True if the task was added, False if the ThreadPool is shutting down.
        """
        if not self.shutdown_event.is_set():
            with self.lock:
                self.task_queue.put(task)
                self.new_job_event.set()
            return True
        else:
            return False

    def check_threads(self) -> bool:
        """
        Debug function, useful for checking thread status
        """
        for thread in self.threads_list:
            if thread.is_alive():
                print(f"Thread {thread.name} is alive")
                return True
            else:
                print(f"Thread {thread.name} is dead")
        return False


class TaskRunner(Thread):
    """
    Custom TaskRunner implementation
    """

    def __init__(
        self, shutdown_event: Event, task_queue: Queue, lock: Lock, new_job_event: Event
    ):
        super().__init__()
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
        while True:
            self.new_job_event.wait()

            if self.shutdown_event.is_set() and self.task_queue.empty():
                break

            with self.lock:
                if self.task_queue.empty():
                    self.new_job_event.clear()
                    continue

                task = self.task_queue.get()

            result = task.solve()
            self.save_result(result, task.id)
