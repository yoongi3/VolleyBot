from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
channel_ID = int(os.getenv("CHANNEL_ID"))

# Initialize bot
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

OPENING_MSG = """
-------------------
:volleyball: **VolleyBot** :volleyball:
-------------------
Finds court availability at [Olympic Park Sports Hall](https://secure.activecarrot.com/public/facility/browse/487/1848).
- **Weekdays:** Filters out courts that can't be booked past 7PM.
- **Weekends:** All times available.
*Commands:*
- `?courts [X]` : Court availability for the next [X](default 7) days.
- `?next [Y] [X]` : Court availability starting [Y](default 1) weeks ahead for the next [X](default 7) days.
"""

# Define the message to send when the bot is ready
async def send_welcome_message():
    channel = bot.get_channel(channel_ID)
    await channel.send(OPENING_MSG)

@bot.command(name="clear", help="Clears the specified number of messages (default is 10).")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    if amount < 1:
        await ctx.send("Please specify a number greater than 0.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=3)


# Register events and commands
@bot.event
async def on_ready():
    print ("hello, ready to go")
    await send_welcome_message()

# Import and add commands from other files
from Commands.court_availability import courts, next

bot.add_command(courts)
bot.add_command(next)

# Run the bot
bot.run(bot_token)