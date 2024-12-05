from manager import Manager, Task
from mcbot import MCBot
from flask import Flask, render_template
from time import sleep
manager = Manager()

app = Flask("HiveMine")

@app.route('/')
def root():
    return render_template("index.html", title="HiveMine")

@app.route('/tasks')
def tasks():
    return "<br>".join([task.name for task in manager.tasks.queue])

num = 0
@app.route('/add_task')
def add_task():
    global num
    manager.queue(Task(f"Demo Task {num}", demo_task, num))
    num += 1
    return "Done"

@app.route('/add_many_tasks')
def add_many_tasks():
    global num
    i = 0
    while i < 20:
        manager.queue(Task(f"Demo Task {num}", demo_task, num))
        i += 1
        num += 1
    return "Done"


def run():
    MCBot(f"HiveMineAgent", manager, is_king = True)
    print("You can access the task list at 127.0.0.1:5000/tasks") # TODO: figure out how to read url/port dynamically
    print("You can add a single demo task at 127.0.0.1:5000/add_task")
    print("You can add 20 demo tasks at 127.0.0.1:5000/add_many_tasks")
    app.run()

def demo_task(bot_obj, num):
    sleep(0.2)
    bot_obj.bot.chat(f"I have completed the demo task! ({num})")

if __name__ == '__main__':
    run()