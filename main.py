from javascript import require, On, off
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

RANGE_GOAL = 3
SERVER_IP = '127.0.0.1'
SERVER_PORT = 25565
BOT_ARGS = {
    'host': SERVER_IP,
    'port': SERVER_PORT
  }


class MCBot:
  def __init__(self, bot_name, bot_args = BOT_ARGS):
     self.bot_args = {
        'host': bot_args['host'],
        'port': bot_args['port'],
        'username': bot_name
     }
     self.reconnect = True
     self.bot_name = bot_name
     self.start_bot()

  def start_bot(self):
    self.bot = mineflayer.createBot(self.bot_args)
    self.bot.loadPlugin(pathfinder.pathfinder)
    print(f"Started mineflayer but with the name {self.bot_name}")
    self.start_listeners()

  def start_listeners(self):
    @On(self.bot, 'login')
    def handle_login(this):
        bot_socket = self.bot._client.socket
        print(
            f"Logged in to {bot_socket.server if bot_socket.server else bot_socket._host }"
        )

    @On(self.bot, 'spawn')
    def handle_spawn(this):
      print("I spawned 👋")

    @On(self.bot, 'chat')
    def handle_chat(this, sender, message, *args):
      print(f"{self.bot_name} got a message: {sender}> {message}")
      if sender and (sender != self.bot_name) and (message.startswith(f"{self.bot_name}: ") or (message.startswith(f"Bots: "))):
        command = " ".join(message.split(' ')[1:])
        if 'come' in command:
          player = self.bot.players[sender]
          print("Target", player)
          target = player.entity
          if not target:
            self.bot.chat("I don't see you !")
            return

          pos = target.position
          movements = pathfinder.Movements(self.bot)
          movements.canDig = False
          self.bot.pathfinder.setMovements(movements)
          self.bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))

        if 'quit' in command:
            self.reconnect = False
            self.bot.quit()
            
    @On(self.bot, "kicked")
    def handle_kicked(this, reason, loggedIn):
        if loggedIn:
            print(f"Kicked from server: {reason}")
        else:
            print(f"Kicked whilst trying to connect: {reason}")

    @On(self.bot, "end")
    def handle_end(this, reason):
        print(f"Disconnected: {reason}")
        
        # Turn off event listeners
        off(self.bot, "login", handle_login)
        off(self.bot, "kicked", handle_kicked)
        off(self.bot, "spawn", handle_spawn)
        off(self.bot, "chat", handle_chat)
        if self.reconnect:
          print("Bot restarting...")
          print(self.bot_name)
          self.start_bot()
        off(self.bot, "end", handle_end)

for i in range(5): 
  bot = MCBot(f"bot{i}")