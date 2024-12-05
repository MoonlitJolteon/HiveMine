# HiveMine: A Minecraft hivemind
HiveMine is a work in progress bot that employs mineflayer as a primary backend for working within a minecraft world. While MineFlayer is a javascript library, HiveMine uses the javascript package for python to be able to load it

### Prerequirements
- Python 3.8+
- Required dependencies listed in requirements.txt
### Installation
Clone the Repository
```bash
git https://github.com/MoonlitJolteon/hivemine
cd hivemine
```
Create the virtual environment for it to run in
```bash
python -m venv venv
source venv/bin/activate
# On Windows, use `venv\Scripts\activate` instead
```
Install dependencies
```bash
pip install -r requirements.txt
```
To start the program, first ensure that you are running a 1.20.1 minecraft server in offline mode on your local machine. Alternatively, you can also launch a single player world and open it to lan specifying 25565 as the port.<br>
Next, simply start the bot by running.
```bash
python main.py
```
You can access the web server based controls at the following addresses (heavily WIP, currently going to the URL activates it)

- List the tasks currently in queue: [127.0.0.1:5000/tasks](127.0.0.1:5000/tasks)
- Add an additional demo task to the queue: [127.0.0.1:5000/add_task](127.0.0.1:5000/add_task)
- Add 20 demo tasks to the queue: [127.0.0.1:5000/add_many_tasks](127.0.0.1:5000/add_many_tasks)