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
    return "<br>".join([task.name for task in manager.queue.queue])

num = 0
@app.route('/add_task')
def add_tasks():
    global num
    manager.queue(Task(f"Task {num}", demo_task, num))
    num += 1
    return "Done"


def run():
    for i in range(1):
        MCBot(f"bot{i}", manager, is_king = (i == 0))
    app.run()

def demo_task(num):
    sleep(1)
    print(f"Task {num}")

if __name__ == '__main__':
    run()