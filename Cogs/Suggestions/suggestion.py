import discord
from discord.ext import commands
from discord import app_commands as slash, Interaction, Colour as c
from modules import Console
console = Console()
from discord import ui, ButtonStyle
from datetime import datetime

class SuggestionView(ui.View):
    def __init__(self, title:str, suggestion:str, attachment: discord.Attachment):
        super().__init__(timeout=None)
        self.title = title
        self.suggestion = suggestion
        self.attachment = attachment

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        self.stop()
        try:
            channel = interaction.guild.get_channel(1283319898537459723)
            if self.attachment:
                await channel.create_thread(name=self.title, content=f"- Suggest by {interaction.user.mention}\n> {self.suggestion}", file=await self.attachment.to_file())
            else:
                await channel.create_thread(name=self.title, content=f"- Suggest by {interaction.user.mention}\n> {self.suggestion}", embed=discord.Embed().set_image(url="https://i.pinimg.com/736x/c5/0b/33/c50b33134d0acb6ed2a54d4e0bea5270.jpg"))
            return await interaction.response.send_message("Your suggestion has been uploaded.", ephemeral= True, delete_after= 30)
        except Exception as e:
            console.log(f"Error: {e}", "red")
        return

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("Your suggestion has been canceled.", ephemeral=True)
        self.stop()
        return



class Sug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @slash.command(name="suggest", description="Submit your suggestion with a title, description, and optional attachment")
    async def suggest(self, interact: Interaction, title:str, suggestion: str, attachment: discord.Attachment = None):
        if len(title) > 128:
            await interact.response.send_message(f"Title exceeds the 128 character limit!")
            return
        if len(suggestion) > 2048:
            await interact.response.send_message(f"Suggestion exceeds the 2048 character limit!")
            return

        embed = discord.Embed(title="New Suggestion", description="Please confirm your suggestion below", color=discord.Color.blue())
        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Suggestion", value=suggestion, inline=False)
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.kD6Sp4NSU6yhNLPuWvHy1AHaHa?rs=1&pid=ImgDetMain")
        try:
            if attachment is not None:
                if attachment.content_type.startswith("image/") or attachment.content_type.startswith("video/"):
                    embed.set_image(url=attachment.url)
                else:
                    await interact.response.send_message(f"Invalid file type! Please attach an image or video.", ephemeral=True)
                    return
        except Exception as e:
            console.log(f"Error: {e}", "red")

        view = SuggestionView(title, suggestion, attachment)
        await interact.response.send_message(embed=embed, view=view, ephemeral= True, delete_after= 180)
    
async def setup(bot):
    await bot.add_cog(Sug(bot))