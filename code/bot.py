# Essenttials für Discord
import discord
from discord.ext import commands
# 
import asyncio
import os
from dotenv import load_dotenv
import json 
# Für die Datenbank und Extra Antworten
#import sqlite3
# Lan
#import spacy

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
"""
# Für die Datensammliung vom Menschlichen Support
connection = sqlite3.connect('chat_database.db')

# Object erstellung für die Datenbank
cursor = connection.cursor()

# SQl Befehle für die Erstellung der Datenbank
cursor.execute('CREATE TABLE messages (id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT, timestamp INTEGER)')
connection.commit()
"""

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
    await achannel.send("Hewwo I am online")
    
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
        # might change to "thread.channel"
        return msg.author == ctx.author and msg.channel == thread

    async def wait():
        user_response = await bot.wait_for('message', check=check, timeout=300)
        problem = user_response.content.lower()
        return problem

    async def request_support(ctx, thread):
            role_id = support_id  # Replace ROLE_ID with the actual role ID to mention
            role = ctx.guild.get_role(role_id)
        
            if role:
                for member in role.members:
                    await thread.add_user(member)
            await thread.send(f"Hey <@1115553886627971082>! {ctx.author} needs some help!")
            
    async def yes_or_no():
            await thread.send("Please only answer with Yes or No")
    try:
        problem = await wait()

        #Keywordbasierte Antworten und Weiterleitung des Problems
        if 'internet' in problem:
            await thread.send("I see you are having problems with your internet. Have you tried restarting your router?")
            await yes_or_no()
            problem = await wait()
            if 'yes' in problem:
                await thread.send("Sorry i can not help you anymore, i am requesting support!")
                await request_support(ctx, thread)
            else:
                await thread.send("Please restart your router and come back for help if you need any!")
                
        elif 'printer' in problem:
            await thread.send("Make sure the printer is turned on and properly connected to your computer.")
        elif 'email' in problem:
            await thread.send("Check your email settings and ensure you have a stable internet connection.")
        elif 'headset' in problem:
            await thread.send("I see you are having problems with your headset. If it is a USB Headset, check if it is connected to your computer or your dockingstation. If it is a bluetooth headset, check if it is connected and charged (sounds of the headset and lights are good indicators!)")
        else:
            await thread.send("I'm sorry, I'm not sure how to help with that problem. I'll get human help!")




    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond...")

bot.run(Discord_TOKEN)
