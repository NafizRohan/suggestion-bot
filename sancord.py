import discord
from discord.ext import commands
from pathlib import Path
from modules import Console
import time

console = Console()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_all_cogs(directory: str):
    cogs_dir = Path(directory)
    for cog_file in cogs_dir.rglob('*.py'):
        if cog_file.name.startswith('_'):
            continue
        cog_path = cog_file.with_suffix('')
        module_path = str(cog_path).replace('/', '.').replace('\\', '.')

        try:
            await bot.load_extension(module_path)
            console.log(f"Cogs loaded: {module_path}", color='green')
        except Exception as e:
            console.log(f"Error: Failed to load {module_path}: {e}", color='red')

@bot.event
async def on_ready():
    console.log(f'{bot.user} logged in successfully.', color='green')
    console.log("Initializing cogs, please hold...", color="yellow")
    time.sleep(1)
    await load_all_cogs('./Cogs')
    console.log("Syncing slash commands with the server...", color="blue")
    time.sleep(1)
    try: # Sync all slash(/) commands. Must needed
        synced = await bot.tree.sync()
        console.log(f"Sync complete. {len(synced)} command(s) synced successfully.", "green")
    except Exception as e:
        console.log("Error: Failed to sync slash commands.", "red")
        console.log(f"Error: {e}", "red")


TOKEN = "MTI4MjY3MzAyMTI5MDU0OTMxOQ.GvvX75.f7yU5eMzewCbUvotZbWrpL7ZC7yii5k1OjFSNg"
bot.run(TOKEN, log_handler= None)
