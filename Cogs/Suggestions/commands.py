import discord
from discord.ext import commands
from discord import app_commands as slash, Interaction, Colour as c
from modules import Console
console = Console()

class Sug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @slash.command(name="suggest", description="Write down your suggestion here")
    async def suggest(self, interact:Interaction, suggestion:str):
        if not suggestion:
            return
        else:
            
            console.log(f"Suggestion: {suggestion} from **{interact.user}**", "cyan")
    
async def setup(bot):
    await bot.add_cog(Sug(bot))