import config
import discord
from discord import app_commands as ac
from discord import Colour as c
from discord import Interaction, ui
from discord.ext import tasks
import mysql.connector as sql
from prettytable import PrettyTable
import random
from samp_client.client import SampClient as GTA
import time
from typing import Optional
#Client Setup
client = discord.Client(intents = discord.Intents.all())
bot = ac.CommandTree(client = client)
#Database Setup
databaseinfo = {'user': config.USERNAME, 'password': config.PASSWORD, 'host': config.HOSTNAME, 'database': config.DATABASE, 'raise_on_warnings': True}
#Timestamp
time_ = time.localtime()
timestamp = f"[{time_.tm_hour}:{time_.tm_min}:{time_.tm_sec}]  "
#Defines
def write_log(log: str):
    try:
        with open(config.LOG_PATH, "a+t") as lw:
            lw.write(f"{timestamp}{log}\n")
            return print(f"{timestamp}{log}")
    except Exception as e:
        raise print(f"{timestamp}{e}")
    
def ConnectToDatabase():
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        print(f"{timestamp}MySQL Connection Created Successfully")
    except Exception as e:
      print(f"{timestamp}Could not connect to MySQL DataBase. Exitting...")
      write_log(e)
      exit()


def sql_query(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        knowledgebase.commit()
        print(f"{timestamp}Sql query is executed with no errors and the query is '**{query}**'")
        write_log(f"'{query}' this query is executed.")
        return 1
    except Exception as e:
        print(f"{timestamp}{e}")
        write_log(f"'{query}' isn't executed fully beacuse '{e}'")
        return 0

def GetSqlResult(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"{timestamp}SanCord got the query result!")
        write_log(f"sanCord got the query result of '{query}'")
        return result
    except Exception as e:
        print(f"{timestamp}{e}")
        return write_log(f"SanCord can't execute '{query}' this query becasue: {e}")

def checkId(query):
    try:
        knowledgebase = sql.connect(**databaseinfo)
        cursor = knowledgebase.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        print(f"{timestamp}I got the result of this query '{query}'")
        write_log(f"I got the result of this query '{query}'")
        return result
    except Exception as e:
        print(f"{timestamp}{e}")
        return write_log(f"I can't execute this query '{query}'. Reason is '{e}'")
    
def GetGuildSerial(guild_id: int):
    query = GetSqlResult(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
    if not query:
        return 'NULL'
    for i in query:
        serial = i[0]
    return serial

async def Status(channel_id: Optional[int] = 1108983291018739755, ip: Optional[str] = "127.0.0.1", port: Optional[int] = 7777, footer_text: Optional[str] = None):
    try:
        list = PrettyTable(['USERNAME    ', '  PING'])
        list.align['USERNAME    '] = "l"#[left align]
        list.align['  PING'] = "r"#[right align]

        #list2
        list2 = PrettyTable(['USERNAME    ', '  PING'])
        list2.align['USERNAME    '] = "l"#[left align]
        list2.align['  PING'] = "r"#[right align]

        #list3
        list3 = PrettyTable(['USERNAME   ', '  PING'])
        list3.align['USERNAME   '] = "l"#[left align]
        list3.align['  PING'] = "r"#[right align]

        #list4
        list4 = PrettyTable(['USERNAME    ', '  PING'])
        list4.align['USERNAME    '] = "l"#[left align]
        list4.align['  PING'] = "r"#[right align]
        error = discord.Embed(title= "Runtime Error", color= c.red())
        time.sleep(1)
        try:
            samp = GTA(address= ip, port= port)
            samp.connect()
            info = samp.get_server_info()
        except Exception as e:
            error.add_field(name= 'IP ADDRESS', value= f"```{ip}:{port}```")
            error.add_field(name= 'Status', value= "```Offline!```")
            error.add_field(name="Information", value= "```diff\n- Could not connect with server....```", inline= False)
            error.set_thumbnail(url= "R:/_SanCord/Stuffs/red_alert.png")
            error.set_footer(text= footer_text)
            write_log(e)
            return error
        #If No Error On Connection
        online = info.players
        max_players = info.max_players
        host = info.hostname
        language = info.language
        players = [samp.name for samp in samp.get_server_clients_detailed()]
        ping = [samp.ping for samp in samp.get_server_clients_detailed()]
        status = discord.Embed(title= host, color= c.green())
        status.add_field(name= "IP ADDRESS", value= f"```\n{ip}:{port}\n```",inline= False)
        status.add_field(name= "Status", value= "```\n✅Online!\n```", inline= True)
        status.add_field(name= "Players", value= f"```\n{online}/{max_players}\n```", inline= True)
        status.add_field(name= "Language", value= f"```\n{language}\n```", inline= True)
        if online == 0:
            status.add_field(name="City Status", value= "```diff\n- No Players Are Playing:(```", inline= False)
            return status
        if online == 100:
            status.add_field(name= "City Status", value= "```css\nWe Reached 100 Players In Our Server, Thats Great!", inline= False)
            return status
        if online > 100:
            status.add_field(name="City Status", value="```css\nHurrah! We Reached More Then 100 Players.```", inline= False)
            return status
        if online > 0 and online < 100:
            if online < 21:
                for i in range(online):
                    list.add_row([players[i], ping[i]])
                value = f"```\n{list}\n```"
                status.add_field(name= "Current Players", value= value, inline= False)            
            if online > 20 and online < 41:
                for i in range(0,20):
                    list.add_row([players[i], ping[i]])
                value0 = f"```\n{list}\n```"
                status.add_field(name= "Current Players", value= value0, inline= False)
                for i in range(20,online):
                    list2.add_row([players[i], ping[i]])
                value1 = f"```\n{list2}\n```"
                status.add_field(name= "Current Players", value= value1, inline= False)           
            if online > 40 and online < 61:
                for i in range(0,20):
                    list.add_row([players[i], ping[i]])
                value00 = f"```\n{list}\n```"
                status.add_field(name= "Current Players", value= value00, inline= False)
                for i in range(20,40):
                    list2.add_row([players[i], ping[i]])
                value11 = f"```\n{list2}\n```"
                status.add_field(name= "Current Players", value= value11, inline= False)
                for i in range(40, online):
                    list3.add_row([players[i], ping[i]])
                value22 = f"```\n{list3}\n```"
                status.add_field(name= "Current Players", value= value22, inline= False)
            if online > 60 and online < 81:
                for i in range(online):
                    list.add_row([players[i], ping[i]])
                value000 = f"```\n{list}\n```"
                status.add_field(name= "Current Players", value= value000, inline= False)
                for i in range(online):
                    list2.add_row([players[i], ping[i]])
                value111 = f"```\n{list2}\n```"
                status.add_field(name= "Current Players", value= value111, inline= False)
                for i in range(online):
                    list3.add_row([players[i], ping[i]])
                value222 = f"```\n{list3}\n```"
                status.add_field(name= "Current Players", value= value222, inline= False)
                for i in range(online):
                    list4.add_row([players[i], ping[i]])
                value333 = f"```\n{list4}\n```"
                status.add_field(name= "Current Players", value= value333, inline= False)
            if online > 80 and online < 101:
                for i in range(online):
                    list.add_row([players[i], ping[i]])
                value0000 = f"```\n{list}\n```"
                status.add_field(name= "Current Players", value= value0000, inline= False)
                for i in range(online):
                    list2.add_row([players[i], ping[i]])
                value1111 = f"```\n{list2}\n```"
                status.add_field(name= "Current Players", value= value1111, inline= False)
                for i in range(online):
                    list3.add_row([players[i], ping[i]])
                value2222 = f"```\n{list3}\n```"
                status.add_field(name= "Current Players", value= value2222, inline= False)
                for i in range(online):
                    list3.add_row([players[i], ping[i]])
                value3333 = f"```\n{list3}\n```"
                status.add_field(name= "Current Players", value= value3333, inline= False)
                for i in range(online):
                    list4.add_row([players[i], ping[i]])
                value4444 = f"```\n{list4}\n```"
                status.add_field(name= "Current Players", value= value4444, inline= False)
        status.set_footer(text = footer_text)
        time.sleep(2)
        return status
    except Exception as e:
        print(f"{timestamp}{e}")
        return discord.Embed(description= e)

def suggestions(title: str, suggestion_text: str, suggestion_by: str, footer: str, url: str, approved_by: Optional[str] = None):
    suggetion_embed = discord.Embed(title= "New Suggestion!", color= c.gold())
    suggetion_embed.set_author(name= suggestion_by, icon_url=f"{url}")
    suggetion_embed.set_thumbnail(url= client.user.avatar)
    suggetion_embed.add_field(name= title, value= suggestion_text)
    suggetion_embed.set_footer(text= footer)
    if approved_by != None:
        write_log(f"A suggestion of {suggestion_by} is approved by {approved_by}.")
    return suggetion_embed

def GetSChannel(guild_id: int):
    query = GetSqlResult(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
    for i in query:
        channel = i[10]
    return channel

def GetSuggestChannel(id: int):
    query = GetSqlResult(f"SELECT * FROM guilds WHERE guild_id = {id}")
    for i in query:
        channel = i[9]
    return channel

async def GetSuggestion(id: int):
    query = GetSqlResult(f"SELECT * FROM suggestions WHERE author = {id}")
    for i in query:
        key = i[1]
        guild_id = i[2]
        title = i[4]
        suggestion = i[5]
        member_id = i[3]
    guild = client.get_guild(int(guild_id))  
    member = guild.get_member(int(member_id))
    embed = suggestions(title= title, suggestion_text= suggestion, suggestion_by= member, footer= f"If you want to approve it type /approve {key} else type /deny {key}", url= member.avatar)    
    return embed

#Loops
@tasks.loop(seconds= 30)
async def AutoStatus():
    query = GetSqlResult("SELECT * FROM guilds WHERE status = 1")
    for i in query:
        guild_id = i[1]
        channel_id = i[3]
        ip = i[5]
        port = i[6]
        guild = await client.fetch_guild(guild_id)
        try:
            channel =  await client.fetch_channel(channel_id)
        except Exception as e:
            print(e)
            continue
        await channel.purge(limit= 5)
        embeds = await Status(channel_id= int(channel_id), ip= ip, port= port, footer_text= f"Status Refreshed in botry 30 seconds\nLast Refreshed at {time_.tm_hour}:{time_.tm_min}:{time_.tm_sec}")
        embeds.set_thumbnail(url= guild.icon)
        await channel.send(embed= embeds)
        return

##_________________________________##
##__________CILENT EVENT__________##
@client.event
async def on_ready():
    ConnectToDatabase()
    AutoStatus.start()
    print(f"{timestamp}{client.user.name} is activated.")
    try:
        synced = await bot.sync()
        print(f"{timestamp}{client.user.name} has synced {len(synced)} command(s)")
    except Exception as e:
        print(f"{timestamp}I Cannot sync any command(s) because of {e}")
    write_log(f"{client.user.name} is activated. {client.user.name} has synced {len(synced)} command(s)")
    return 

@client.event
async def on_guild_join(guild):
    try:
        guild_id = guild.id
        guild_name = guild.name
        sql_query(f"INSERT INTO guilds (`guild_id`, `guild_name`, `joining_date`) VALUES (\"{guild_id}\", \"{guild_name}\",  NOW())")
        write_log(log= f"Guild's Information Added To Database(Guild id: {guild_id}, Guild name: {guild.name}, Serial Number: {GetGuildSerial(guild_id= guild_id)})")
        print(f"{timestamp}Guild Is Added To Database.")
    except Exception as e:
        print(f"{timestamp}{e}")
        write_log("Hey Nafis, I got a serious error. I can't store guild data on a guild join.")
    return

@client.event
async def on_guild_remove(guild):
    try:
        guild_id = guild.id
        sql_query(f"DELETE FROM guilds WHERE guilds.serial = {GetGuildSerial(guild_id = guild_id)}")
        write_log(f"Guild Is Removed From Database(Guild id: {guild_id}).")
        print(f"{timestamp}Guild Is Removed From Database")
    except Exception as e:
        print(f"{timestamp}{e}")
        write_log("Hey Nafis, I got a serious error. I can't delete guild data on a guild leave.")
    return
    
#######            COMMANDS             #######

class info(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    
    @ui.button(label= "✅| Yes", style= discord.ButtonStyle.green)
    async def yes(self, interaction:Interaction, button: ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(content="Thanks for confirming. You can use SanCord now.")
    
    @ui.button(label= "❌| No", style= discord.ButtonStyle.red)
    async def no(self, interaction:Interaction, button: ui.Button):
        sql_query(f"UPDATE guilds SET ip = 'NULL', port = NULL, set_ip = 0, status_channel = NULL, sg_channel = NULL, sg_logC = NULL, status = 0 WHERE serial = {GetGuildSerial(interaction.user.guild.id)};")
        await interaction.message.delete()
        await interaction.response.send_message(content="Nevermind I will delete this contant", delete_after= 120,ephemeral= True)
        return

class Setup(ui.Modal, title = "Set your server information"):
    ip = ui.TextInput(label= "IP", placeholder="127.0.0.1!",required= True)
    port = ui.TextInput(label= "PORT", placeholder="",required= True)
    suggestion_channel = ui.TextInput(label= "Suggestion Channel", placeholder="Channel ID!",required= True)
    sLog_channel = ui.TextInput(label= "Suggetion Log Channel", placeholder="Channel ID!",required= True)
    Status_Channel = ui.TextInput(label= "Status Channel", placeholder="Channel ID!",required= True)
    async def on_submit(self, interaction: Interaction):
        try:
            await interaction.response.send_message("Setting up.....")
            query = sql_query(f"UPDATE guilds SET ip = '{str(self.ip)}', port = {self.port}, set_ip = 1, status_channel = {self.Status_Channel}, sg_channel = {self.suggestion_channel}, sg_logC = {self.sLog_channel}, status = 1 WHERE serial = {GetGuildSerial(interaction.user.guild.id)};")
            if query == 1:
                information = discord.Embed(title= "Server Infromation", description= f"Are the pieces of information right?\n> 1. Server IP: {self.ip}\n> 2. Server PORT: {self.port}\n> 3. Status Channel: <#{self.Status_Channel}>\n> 4. Suggestion Channel: <#{self.suggestion_channel}>\n> 5. Log Channel: <#{self.sLog_channel}>\n\n`Please confirm this information by pressing \"Yes\" else press \"No\".\nNote: By clicking \"Yes\" Auto-Status will enabled automatically.`", colour= 0x3f88ff)
                await interaction.edit_original_response(content=f"Hey {interaction.user.mention},\nThanks for choosing me for your server. You submit your very valuable data for setup me. Please confirm your information again.", embed= information, view= info())
            else:
                await interaction.edit_original_response("Someting went wrong. Please try again...")
                return
        except Exception as e:
            print(f"{timestamp}{e}")
            write_log(f"SanCord got this error '{e}' on /setup command")
            await interaction.response.send_message(e) 
        return
                   
@bot.command(name= "setup", description= "Set up me for your server!")
@ac.checks.has_permissions(manage_guild = True)
@ac.checks.bot_has_permissions(send_messages = True)
async def setup(interaction:Interaction):
    await interaction.response.send_modal(Setup())
    return

@bot.command(name= "player-status", description= "Show Player Status")
async def initiat(interaction:Interaction):
    guild_id = interaction.user.guild.id
    output = GetSqlResult(f"SELECT * FROM guilds WHERE serial = {GetGuildSerial(guild_id= guild_id)}")
    if not output:
        await interaction.response.send_message(f"Cannot Find Your Guild In Database. Invite SanCord Againg To Add Your Guild In SanCord Database.")
        return
    for i in output:
        ip = i[5]
        port = i[6]
    if ip == "NULL" or port == "NULL":
        await interaction.response.send_message(f"At First Set Your IP. Use `/setip`")
        return
    channel_id = interaction.channel.id
    channel = await interaction.guild.fetch_channel(channel_id)
    await interaction.response.send_message(f"Getting Information. Please wait.......")
    stat = await Status(channel_id= int(channel_id), ip= ip, port= port, footer_text= None)
    stat.set_thumbnail(interaction.guild.icon)
    await interaction.delete_original_response()
    time.sleep(0.1)
    await channel.send(f"{interaction.user.mention} Here is the current player status of `{ip}:{port}`", embed= stat)
    return

@bot.command(name= "server", description= "Show Server Info")
async def server(interaction:Interaction):
    try:
        result = GetSqlResult(f"SELECT * FROM guilds WHERE serial = {GetGuildSerial(guild_id= interaction.user.guild.id)}")
        if not result:
            await interaction.response.send_message("Cannot Find Your Guild In Database. Invite SanCord Againg To Add Your Guild In SanCord Database.")
            return
        for i in result:
            ip = i[5]
            port = i[6]
        try:
            samp = GTA(address= ip, port= port)
            samp.connect()
        except Exception as e:
            await interaction.response.send_message(e)
            return
        else:
            info = samp.get_server_info()
            rulevalue = [rule.value for rule in samp.get_server_rules()]
            host = info.hostname
            player = info.players
            max_players = info.max_players
            lang = info.language
            gamemode = info.gamemode
            locked = info.password
            map = rulevalue[1]
            url = rulevalue[4]
            if locked == False:
                locked = 'No'
            else:
                locked = 'Yes'
            server = discord.Embed(title=f"{host}",color= c.green())#embed creation
            server.set_thumbnail(url= interaction.user.guild.icon)
            server.add_field(name="Name", value= f"> [{host}](https://{url})", inline= True)
            server.add_field(name="Players", value= f"> {player}/{max_players}", inline= True)
            server.add_field(name="Language", value= f"> {lang}", inline= True)
            server.add_field(name= "Version", value= f"> {gamemode}", inline= True)
            server.add_field(name="Locked", value= f"> {locked}")
            server.add_field(name="Map", value= f"> {map}")
            
            #Sending embed
            await interaction.response.send_message(embed= server)
            return#End
    except Exception as e:
        await interaction.response.send_message(e)
        write_log(f"{e}. On /server command")
    
class st_sure(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    
    @ui.button(label= "✅| Yes", style= discord.ButtonStyle.green)
    async def yes(self, interaction:Interaction, button: ui.Button):
        sql_query(f"UPDATE guilds SET status = 1 WHERE serial = {GetGuildSerial(interaction.guild.id)}")
        await interaction.message.delete()
        await interaction.response.send_message(content=f"Okay {interaction.user.mention}, Auto-Status System is now enabled for your server.", delete_after= 120,ephemeral= True)
        return
    
    @ui.button(label= "❌| No", style= discord.ButtonStyle.red)
    async def no(self, interaction:Interaction, button: ui.Button):
        sql_query(f"UPDATE guilds SET status = 0 WHERE serial = {GetGuildSerial(interaction.guild.id)}")
        await interaction.message.delete()
        await interaction.response.send_message(content="Nevermind I will delete this contant", delete_after= 120,ephemeral= True)
        return

@bot.command(name= "status", description= "Turn no or off status system")
async def status(interaction:Interaction):
    embed = discord.Embed(title= "Auto-Status System", color= c.green())
    embed.add_field(name = "",value= "If you want to turn on Auto-Status System simply press \"Yes\" or press \"No\" to turn it off.")
    await interaction.response.send_message(embed= embed, view= st_sure())
    return

#Commands of Suggestion System
class sure(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    
    @ui.button(label= "✅| Yes", style= discord.ButtonStyle.green)
    async def yes(self, interaction:Interaction, button: ui.Button):
        try:
            embed = await GetSuggestion(interaction.user.id)
            channel_id = GetSChannel(interaction.guild.id)
            id = await interaction.guild.fetch_channel(channel_id)
            await id.send(embed= embed)
            await interaction.message.delete()
            await interaction.response.send_message(content="Your Suggestion is submitted. Now wait for approve.", delete_after= 120,ephemeral= True)
        except Exception as e:
            print(e)
    
    @ui.button(label= "❌| No", style= discord.ButtonStyle.red)
    async def no(self, interaction:Interaction, button: ui.Button):
        sql_query(f"DELETE FROM suggestions WHERE author = {interaction.user.id}")
        await interaction.message.delete()
        await interaction.response.send_message(content="Nevermind I will delete this contant", delete_after= 120,ephemeral= True)
        return
        
class suggestion(ui.Modal, title = "Suggest Your Idea"):
    title1 = ui.TextInput(label= "Title", style= discord.TextStyle.short, placeholder= "Place A Title", required= True, min_length= 0, max_length= 256)
    suggestion = ui.TextInput(label= "Suggestion", style= discord.TextStyle.paragraph, placeholder= "Place Your Idea", required= True, min_length= 1, max_length= 1024)
    async def on_submit(self, interaction: Interaction, /) -> None:
        try:
            key = random.randint(1000000,15000000)
            sql_query(f"INSERT INTO suggestions (`guild_id`, `title`, `suggestion`, `s_time`, `author`, `key`) VALUES({interaction.user.guild.id}, \"{self.title1}\", \"{self.suggestion}\", NOW(), \"{interaction.user.id}\", \"{key}\")")
            embed = discord.Embed(title= "Are you Sure?", description= f"{self.suggestion}" + "\n\nAre you sure to confirm this suggetion? If yes then press **Yes** else press **No**.")
            embed.set_thumbnail(url= "https://discord.com/channels/1075731913580490764/1094965559755538483/1116021152201052230")
            await interaction.response.send_message(embed= embed, view= sure())
        except Exception as e:
            print(e)
        return 
    
@bot.command(name= "suggest", description= "Suggest Your Idea")
@ac.checks.bot_has_permissions(manage_messages = True)
async def suggest(interaction:Interaction):
    query = checkId(f"SELECT COUNT(*) AS count FROM suggestions WHERE guild_id = {interaction.user.guild.id} AND author = {interaction.user.id}")
    if query[0] == 0:
        await interaction.response.send_modal(suggestion())
        return
    else:
        await interaction.response.send_message("You already suggest your Idea. You can't suggest any more idea until any modaretor approve or deny your current suggestion.", delete_after= 120, ephemeral= True)
        return

@bot.command(name= "approve", description= "Approve a suggestion")
@ac.checks.bot_has_permissions(manage_messages = True)
async def approve(interaction:Interaction, id:int):
    query = GetSqlResult(f"SELECT * FROM suggestions WHERE key = {id}")
    if not query:
        await interaction.response.send_message(content="This suggestion is not approved. Because suggestion id is invalid.", ephemeral= True)
        return
    
    for i in query:
        author = i[3]
        title = i[4]
        text = i[5]
    guild = client.get_guild(interaction.guild.id)
    member = guild.get_member(int(author))
    embed = suggestions(title= title, suggestion_text= text, suggestion_by= member, footer= "If you want to support press ✅ else press ❌",url= member.avatar, approved_by= interaction.user.name)
    channel_id = GetSuggestChannel(interaction.guild.id)
    channel = await interaction.guild.fetch_channel(channel_id)
    await interaction.response.send_message("Approved!")
    sms = await channel.send(embed= embed)
    await sms.add_reaction("✅")
    await sms.add_reaction("❌")
    write_log(f"{interaction.user.name} approved a suggestion in {interaction.guild.name}")
    return sql_query(f"DELETE FROM suggestions WHERE key = {id}")

@bot.command(name= "deny", description= "Deny a suggestion")
@ac.checks.bot_has_permissions(manage_messages = True)
async def deny(interaction:Interaction, id:int):
    try:
        sql_query(f"DELETE FROM suggestions WHERE key = {id}")
        await interaction.response.send_message("Suggestion is denied & deleted from my database.")
        write_log(f"{interaction.user.name} delete a suggestion from {interaction.guild.name}")
    except Exception as e:
        await interaction.response.send_message("Invalid id. try again.")
        return
##_________________________________##
##________CLIENT ACTIVATION________##
try:
    client.run(config.TOKEN, reconnect= True, log_handler= None)
except Exception as e:
    print(f"{timestamp}SanCord cannot connect with discord because of {e}")
    write_log(e)