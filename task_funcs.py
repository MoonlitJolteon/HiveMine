from javascript import require
from simple_chalk import chalk
from time import sleep
import threading
pathfinder = require('mineflayer-pathfinder')

def dig_with_wait(bot, block):
    finished = threading.Event()
    def on_dig_complete(err):
        if err:
            bot.chat("Failed to dig block!")
        else:
            bot.chat("Successfully dug block!")
        finished.set()  # Unblock the thread

    bot.dig(block, on_dig_complete)
    finished.wait()  # Block until the dig operation completes


def collect_wood(bot_obj, quantity):
    bot = bot_obj.bot
    def process_found_wood(err, blockPoints):
        if err:
            bot.chat("Error finding oak logs!")
            return
        for block in blockPoints:
            bot.chat(f"Found oak log at {block.position}")
            pos = block.position
            bot.pathfinder.goto(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z), lambda: dig_with_wait(bot, block))
            sleep(5)
            

    bot_obj.log(chalk.magenta(f"Collecting {quantity} oak wood..."))
    bot.findBlock({
        "point": bot.entity.position,
        "matching": bot.registry.blocksByName["oak_log"].id
    }, process_found_wood)

def print_inventory(bot_obj):
    bot = bot_obj.bot
    inv = list(bot.inventory.items())
    bot.chat("My inventory contains [")
    for i in range(len(inv)):
        bot.chat(f"Item {i+1}: {inv[i].displayName} x{inv[i].count}")
    bot.chat("]")
    
def place_crafting_table(bot_obj):
    bot = bot_obj.bot
    # Check if the bot has a crafting table in its inventory
    crafting_table_id = bot.registry.itemsByName["crafting_table"].id
    crafting_table_count = bot.inventory.count(crafting_table_id)
    
    if crafting_table_count > 0:
        # Get the bot's current position
        pos = bot.entity.position
        # Define the position directly below the bot (y - 1)
        target_pos = {'x': pos.x, 'y': pos.y - 1, 'z': pos.z}
        
        # Get the block at the target position
        target_block = bot.world.getBlock(target_pos)
        
        # If the block below is empty (not a solid block), place the crafting table
        if target_block and target_block.name == 'air':
            # Place the crafting table at the target position
            bot.placeBlock(target_pos, bot.registry.itemsByName["crafting_table"], None, lambda err: place_callback(err, bot))
        else:
            bot.chat("Cannot place crafting table, position is blocked.")
    else:
        bot.chat("No crafting table in inventory to place.")


def craft_item(bot_obj, item_name, quantity=1):
    bot = bot_obj.bot

    def on_craft_complete(err):
        if err:
            bot.chat(f"Failed to craft {item_name}: {err}")
        else:
            bot.chat(f"Successfully crafted {quantity} {item_name}(s).")

    try:
        try:
            # Get the item details from the bot's registry
            item = bot.registry.itemsByName[item_name]
            item_id = item.id
            bot.chat(f"Attempting to craft {item.displayName} with ID {item_id}...")
        except KeyError:
            bot.chat(f"Unknown item: {item_name}.")
            return
        
        recipe = bot.recipesFor(item_id, None, quantity, bot.inventory)
        if len(list(recipe)) < 1:
            bot.chat(f"No available recipe for {item_name} with the items I have.")
            return

        # Check if a crafting table is required
        if recipe[0].requiresTable and not bot.inventory.count(bot.registry.itemsByName["crafting_table"].id):
            bot.chat(f"Crafting {item_name} requires a crafting table. I don't have one.")
            return

        # Start crafting
        bot.craft(recipe[0], quantity, None, on_craft_complete)
        bot.chat(f"Successfully crafted {item.displayName}")

    except Exception as e:
        bot.chat(f"Error during crafting: {str(e)}")

    


def come(bot_obj, sender):
    bot = bot_obj.bot
    sleep(1)
    player = bot.players[sender]
    bot_obj.log(chalk.magenta(f"Target {player.username}"))
    target = player.entity
    if not target:
        bot_obj.chat(f"I don't see you {player.username}!")
        return
    pos = target.position
    movements = pathfinder.Movements(bot)
    movements.canDig = False
    bot.pathfinder.setMovements(movements)
    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 2))