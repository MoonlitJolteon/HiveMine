from queue import Queue
class Manager:
    def __init__(self):
        self.bots = set()
        self.tasks = Queue()
        # self.tasks.put(Task("Task A", lambda: print("Task A")))
        # self.tasks.put(Task("Task B", lambda: print("Task B")))
        # self.tasks.put(Task("Task C", lambda: print("Task C")))
        # self.tasks.put(Task("Task D", lambda: print("Task D")))
        # self.tasks.put(Task("Task E", lambda: print("Task E")))

    def queue(self, task):
        self.tasks.put(task)
    
    def get_next_task(self):
        if len(self.tasks.queue) > 0:
            return self.tasks.get()
        else:
            return None

    def register_bot(self, name):
        self.bots.add(name)

class Task:
    def __init__(self, name, func, *args):
        self.name = name
        self.func = func
        self.args = args

    def perform_task(self):
        self.func(*self.args)