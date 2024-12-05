from javascript import require, On, off, AsyncTask
from simple_chalk import chalk
from manager import Task
from task_funcs import come, collect_wood, print_inventory, craft_item, place_crafting_table
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder').pathfinder
mineflayerViewer = require('prismarine-viewer').mineflayer
blockFinderPlugin = require('mineflayer-blockfinder')(mineflayer)

SERVER_IP = '127.0.0.1'
SERVER_PORT = 25565
BOT_ARGS = {
    'host': SERVER_IP,
    'port': SERVER_PORT
}

class MCBot:
    def __init__(self, bot_name, manager, bot_args = BOT_ARGS, is_king = False):
        self.bot_args = {
            'host': bot_args['host'],
            'port': bot_args['port'],
            'username': bot_name
        }
        self.manager = manager
        self.manager.register_bot(bot_name)
        self.reconnect = True
        self.bot_name = bot_name
        self.start_bot()
        self.is_king = is_king
        self.mc_data = None
        if is_king:
            mineflayerViewer(self.bot, { 'port': 3007, 'firstPerson': False })

    def log(self, message):
        print(f"{self.bot_name}: {message}")

    def chat(self, message):
        print(chalk.cyan(f"{self.bot_name} sent: {message}"))
        self.bot.chat(message)

    def start_bot(self):
        self.bot = mineflayer.createBot(self.bot_args)
        self.bot.loadPlugin(pathfinder)
        self.bot.loadPlugin(blockFinderPlugin)
        print(f"Started mineflayer bot with the name {self.bot_name}")
        self.start_listeners()

    def start_listeners(self):
        @On(self.bot, 'login')
        def handle_login(this):
            bot_socket = self.bot._client.socket
            self.log(
            chalk.green(
                f"Logged in to {bot_socket.server if bot_socket.server else bot_socket._host }"
            )
            )

        @On(self.bot, 'spawn')
        def handle_spawn(this):
            self.log("I spawned 👋")

        @AsyncTask(start=True)
        @On(self.bot, 'time')
        def handle_tick_update(this):
            task = self.manager.get_next_task()
            if task:
                task.perform_task()

        @On(self.bot, 'chat')
        def handle_chat(this, sender, message, *args):
            if not self.is_king:
                return
            if sender not in self.manager.bots:
                self.log(f"chat message: {sender}> {message}")

            if sender and (sender != self.bot_name) and (message.startswith(f"~")):
                args = message.split(' ')
                if 'come' in message:
                    self.manager.queue(Task(f"Come to {sender}", come, self, sender))
                
                if 'collect-wood' in message:
                    self.manager.queue(Task(f"Collect {args[1]} wood", collect_wood, self, args[1]))
                
                if 'list-inv' in message:
                    self.manager.queue(Task(f"Listing inventory", print_inventory, self))

                if 'place-table' in message:
                    self.manager.queue(Task(f"Placing crafting table", place_crafting_table, self))

                if 'craft' in message:
                    self.manager.queue(Task(f"Attempting to craft {args[1]}", craft_item, self, args[1]))

                if 'quit' in message:
                    self.reconnect = False
                    self.bot.quit()
                
        @On(self.bot, "kicked")
        def handle_kicked(this, reason, loggedIn):
            if loggedIn:
                self.log(chalk.redBright(f"Kicked from server: {reason}"))
            else:
                self.log(chalk.redBright(f"Kicked whilst trying to connect: {reason}"))

        @On(self.bot, "end")
        def handle_end(this, reason):
            self.log(chalk.red(f"Disconnected: {reason}"))
            
            # Turn off event listeners
            off(self.bot, "login", handle_login)
            off(self.bot, "kicked", handle_kicked)
            off(self.bot, "spawn", handle_spawn)
            off(self.bot, "chat", handle_chat)
            off(self.bot, "time", handle_tick_update)
            if self.reconnect:
                self.log(chalk.blue("Attempting to reconnect"))
                self.start_bot()
            off(self.bot, "end", handle_end)

