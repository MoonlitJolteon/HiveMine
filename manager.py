from queue import Queue
class Manager:
    def __init__(self):
        self.bots = set()
        self.tasks = Queue()

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

    def perform_task(self, bot_obj):
        try:
            self.func(bot_obj, *self.args)
        except Exception as e:
            self.log(e)
        