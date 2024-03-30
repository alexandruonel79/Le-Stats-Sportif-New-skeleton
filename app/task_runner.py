from queue import Queue
from threading import Thread, Event, Lock
import time
import os
from app.Task import Task

class ThreadPool:
    queue: Queue[Task]
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
            #self.num_of_threads =  2


        self.threads = []
        self.queue = Queue()
        self.event = Event()
        self.shutdown = False
        self.shutdown_lock = Lock()  # Lock for accessing shutdown variable
        self.job_states = {}

        print(f"Number of threads: {self.num_of_threads}")

    def start(self):
        for i in range(self.num_of_threads):
            self.threads.append(TaskRunner(self))
            self.threads[i].start()


    def getTask(self) -> Task:
        # coada e concurenta
        return self.queue.get(block= False)

    def submitTask(self, task: Task):
        if self.shutdown != True:
            print(f"Submitting task {task.id}")
            self.job_states[task.id] = {"status": "running"}
            self.queue.put(task)
            self.event.set()
    
    def stop(self):
        with self.shutdown_lock:
            self.shutdown = True

        self.event.set()

        for thread in self.threads:
            thread.join()
    
    # function to check if thread is alive and print the result
    def check_threads(self):
        for thread in self.threads:
            if thread.is_alive():
                print(f"Thread {thread.name} is alive")
            else:
                print(f"Thread {thread.name} is dead")
    
    def get_job_state(self, job_id) -> dict:
        return self.job_states[job_id]
    
    def get_all_jobs_states(self) -> dict:
        # necesita un ochi
        all_jobs_states = {}
        for job_id in self.job_states.keys():
            if self.job_states[job_id]["status"] != "running":
                all_jobs_states[job_id] = "done"
            else:
                all_jobs_states[job_id] = "running"
        return all_jobs_states
    
class TaskRunner(Thread):
    def __init__(self, threadPool: ThreadPool):
        super().__init__()
        self.threadPool = threadPool

    def run(self):
        while True:

            if self.threadPool.shutdown == True and self.threadPool.queue.empty():
                print(f"Thread {self.name} is shutting down")
                break

            self.threadPool.event.wait()

            if self.threadPool.queue.empty():
                self.threadPool.event.clear()
                continue

            task = self.threadPool.getTask()
            result = task.solve()
            # result += f" by thread {self.name}"
            print(f"Task {task.id} solved by thread {self.name}")

            os.makedirs("results", exist_ok=True)
            # save result to disk
            with open(f"results/job_id_{task.id}.txt", "w") as f:
                f.write(str(result))

            # update job state
            self.threadPool.job_states[task.id] = {"status": "done", "data": result}
