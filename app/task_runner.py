from queue import Queue
from threading import Thread, Event, Lock
from app.Task import Task
import time
import os
import json

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        if "TP_NUM_OF_THREADS" in os.environ:
            self.num_of_threads = int(os.environ["TP_NUM_OF_THREADS"])
        else:
            self.num_of_threads =  os.cpu_count()
            #self.num_of_threads = 2
            self.task_queue = Queue()
            self.shutdown_event = Event()
            self.threads_list = []
            self.lock = Lock()
            self.fs_lock = Lock()
            self.shutdown = False
        #print(f"Number of threads: {self.num_of_threads}")

    def start(self):
        for i in range(self.num_of_threads):
            self.threads_list.append(TaskRunner(self.shutdown_event, self.task_queue, self.lock, self.fs_lock))
            self.threads_list[i].start()
    
    def stop(self):
        self.shutdown_event.set()
        self.shutdown = True
        for thread in self.threads_list:
            thread.join()

    def submitTask(self, task: Task) -> bool:
        if not self.shutdown:
            with self.lock:
                #time.sleep(5)
                #print("Adding task to queue")
                self.task_queue.put(task)
            return True  
        else:
            return False

    def get_fs_lock(self) -> Lock:
        return self.fs_lock
    
    def check_threads(self):
        for thread in self.threads_list:
            if thread.is_alive():
                print(f"Thread {thread.name} is alive")
            else:
                print(f"Thread {thread.name} is dead")      

class TaskRunner(Thread):
    def __init__(self, shutdown_event: Event, task_queue: Queue, lock: Lock, fs_lock: Lock):
        # TODO: init necessary data structures
        super().__init__()
        self.shutdown_event = shutdown_event
        self.task_queue = task_queue
        self.lock = lock
        self.fs_lock = fs_lock

    def save_result(self, result, task_id):
        with self.fs_lock:
            os.makedirs("results", exist_ok=True)
            # save result to disk
            with open(f"results/job_id_{task_id}.txt", "w") as f:
                # f.write(str(result))\
                json.dump(result, f)

    
    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            if self.shutdown_event.is_set() and self.task_queue.empty():
                #print(f"Thread {self.name} is shutting down!\n")
                break
            
            with self.lock:
                #time.sleep(5)
                if self.task_queue.empty():
                    #print(f"Thread {self.name} found the queue empty\n")
                    continue
                
                task = self.task_queue.get()
            #print(f"Thread {self.name} is solving the task {task}!\n")
            result = task.solve()
            #time.sleep(5)
            self.save_result(result, task.id)
            #print(f"Thread {self.name} finished the task!\n")


            
