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
        # inainte de pauza
        self.new_job_event = Event()
        #print(f"Number of threads: {self.num_of_threads}")

    def start(self):
        for i in range(self.num_of_threads):
            self.threads_list.append(TaskRunner(self.shutdown_event, self.task_queue, self.lock, self.fs_lock, self.new_job_event))
            self.threads_list[i].start()
    
    def stop(self):
        self.new_job_event.set()
        self.shutdown_event.set()
        for thread in self.threads_list:
            thread.join()
        print("All threads stopped!")

    def submitTask(self, task: Task) -> bool:
        if not self.shutdown_event.is_set():
            with self.lock:
                #time.sleep(5)
                #print("Adding task to queue")
                self.task_queue.put(task)
                self.new_job_event.set()
            return True  
        else:
            return False

    def get_fs_lock(self) -> Lock:
        return self.fs_lock
    
    def check_threads(self) -> bool:
        for thread in self.threads_list:
            if thread.is_alive():
                print(f"Thread {thread.name} is alive")
                return True
            else:
                print(f"Thread {thread.name} is dead")      
        return False

class TaskRunner(Thread):
    def __init__(self, shutdown_event: Event, task_queue: Queue, lock: Lock, fs_lock: Lock, new_job_event: Event):
        # TODO: init necessary data structures
        super().__init__()
        self.shutdown_event = shutdown_event
        self.task_queue = task_queue
        self.lock = lock
        self.fs_lock = fs_lock
        self.new_job_event = new_job_event

    def save_result(self, result, task_id):
        # with self.fs_lock:
        # os.makedirs("results", exist_ok=True)
        # save result to disk
        with open(f"results/job_id_{task_id}.txt", "w") as f:
            # f.write(str(result))\
            json.dump(result, f)
            # f.flush()
            # os.fsync(f.fileno())
        
    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            # print(f"{self.name} is waiting\n")
            self.new_job_event.wait()

            if self.shutdown_event.is_set() and self.task_queue.empty():
                # print(f"{self.name} is shutting down!\n")
                break
            
            with self.lock:
                #time.sleep(5)
                if self.task_queue.empty():
                    # print(f"{self.name} found the queue empty\n")
                    self.new_job_event.clear()
                    continue
                
                task = self.task_queue.get()
                # in pauza
                # if not self.shutdown_event.is_set():
                #     self.new_job_event.clear()

            # print(f"{self.name} is solving the task {task}!\n")
            result = task.solve()
            #time.sleep(5)
            self.save_result(result, task.id)
            #print(f"Thread {self.name} finished the task!\n")

            
