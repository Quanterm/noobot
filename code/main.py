# Essenttials für Discord
import discord
from discord.ext import commands
# 
import asyncio
import os
from dotenv import load_dotenv
import json 
# Für die Datenbank und Extra Antworten
# import sqlite3
# from flair.data import Sentence
# from flair.models import TextClassifier
# connect to SQLite database
# conn = sqlite3.connect('chat_database.db')
# c = conn.cursor()
# # create messages table (if not exists)
# c.execute('''CREATE TABLE IF NOT EXISTS messages
#              (id INTEGER PRIMARY KEY,
#               content TEXT,
#               author TEXT,
#               channel TEXT,
#               timestamp TEXT)''')
#Liste aller benötigten Tokens für adressierte Steuerung
load_dotenv(dotenv_path='./env.env')
Discord_TOKEN = os.getenv('DISCORD_TOKEN')
Discord_TOKEN = str(Discord_TOKEN)
Guild_NAME = os.getenv('GUILD_NAME')
Guild_NAME = str(Guild_NAME)
channel = os.getenv("CHANNEL")
json_path = os.getenv("JSON_PATH")
support_id = os.getenv("SUPPORT_ID")
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.messages = True
# Für Privater Thread mit User 
bot = commands.Bot(command_prefix='!', intents = intents, privileged_intents=True)

#Login des Bots mit Bestätigung in Konsole sowie Bereitmeldung im Support-Channel
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    for guild in bot.guilds:
        if guild.name == str(Guild_NAME):
            break
    else:
        print(f"Could not find {Guild_NAME} guild")
        return

    print(f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')
    achannel = bot.get_channel(int(channel))
    await achannel.send("Hello I am ready to Support! UwU")
    
# Ticketnummer die aufsteigend gezählt wird    
async def save_ticket_count(count):
    with open(json_path, 'r') as f:
        data = json.load(f)
    data['count'] = count
    with open(json_path, 'w') as f:
        json.dump(data, f)

# Lädt die aktuelle Ticketnummer
async def load_ticket_count():
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'count': 1}
    return data['count']    


# Bot-Kommando, der die Supportschleife startet und antwortet
@bot.command(name='support')
async def support(ctx):
    ticket_number = await load_ticket_count()
    
    thread = await ctx.channel.create_thread(name=f'Ticket {ticket_number}')
    await thread.send(f'How can I help you, {ctx.author.mention}? State your problem please.')
    
    ticket_number += 1
    await save_ticket_count(ticket_number)

    def check(msg):
        return msg.author == ctx.author and msg.channel == thread

    async def wait():
        user_response = await bot.wait_for('message', check=check, timeout=600)
        problem = user_response.content.lower()
        return problem

    async def request_support():
        #    role = ctx.guild.get_role(support_id)
        #    if role:
        #        for member in role.members:
        #            await thread.add_user(member)
            await thread.send(f"Hey <@&1115553886627971082> ! {ctx.author.mention} needs some help!")
    
    async def closing_thread():
            await thread.send("No response...Closing Ticket. Open a new one if needed!")
            await thread.edit(archived=True, locked=True)
         #Keywordbasierte Antworten und Weiterleitung des Problems
    try:
        problem = ""
        problem = await wait()

        if 'internet' in problem:
            await thread.send("I see you are having problems with your internet. Have you tried restarting your router?")
            await thread.send("Please only answer with Yes or No")
            problem = await wait()
            if 'yes' in problem:
                await thread.send("Sorry i can not help you anymore. I am requesting support!")
                await request_support()                    
            elif 'no' in problem:
                await thread.send("Please restart your router and come back for help if you need any!")
                problem == None
                problem = await wait()
                if problem != None:
                    await request_support()
                else:
                    await closing_thread()  
            else:
                await thread.send("You did not answer with yes or no...I will give you one more try")
                
        elif 'printer' or 'printing' in problem:
            await thread.send("I see you are having issues with your printer. Which of those Keywords is most accurate for your problem?")
            await thread.send("Ink needed\nconnection problems\n")
            problem = await wait()
            if 'ink' in problem:
                await thread.send("Is some kind of ink missing in the printer?")
                await thread.send("Please only answer with Yes or No")
                problem = await wait()
                if 'yes' in problem:
                    await thread.send("I will request support to order some ink for you")
                    await request_support()
                else:
                    await thread.send("The issue does not seem to be related to ink, i will request some support to help you")
                    await request_support()
            elif 'connection' or 'connecting' in problem:
                await thread.send("If you are having issues connecting to the printer, try both restarting your PC and the printer and come back for help if you need any.")
                problem == None
                problem = await wait()
                if problem != None:
                    await request_support()
                else:
                    await closing_thread()
            else:
                await thread.send("It seems like i can not help you here, I am calling for support!")
                await request_support()

        elif 'email' in problem:
            await thread.send("Check your email settings and ensure you have a stable internet connection.")
        elif 'headset' in problem:
            await thread.send("I see you are having problems with your headset. If it is a USB Headset, check if it is connected to your computer or your dockingstation. If it is a bluetooth headset, check if it is connected and charged (sounds of the headset and lights are good indicators!)")
        else:
            await thread.send("I have not found any keywords, are one of those topics relevant to your problem? Respond with the respective numbers only please")


    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond...")

bot.run(Discord_TOKEN)

