import discord
from discord.ext import commands
import os
import sqlite3
from dotenv import load_dotenv
import json 

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

# connect to SQLite database
conn = sqlite3.connect('chat_database.db')
c = conn.cursor()

# create database table (if not exists)
cursor.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY, name TEXT, role TEXT)''')



#LOGIN
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
    await achannel.send("SQuwuL DAtwa BAwse")
    
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
   

# define on message event listener
@bot.event
async def on_message(message):
    # insert new message into database
    c.execute('''INSERT INTO messages (content, author, channel, timestamp)
                 VALUES (?, ?, ?, ?)''',
              (message.content, message.author.name, message.channel.name, str(message.created_at)))
    conn.commit()
    achannel = bot.get_channel(int(channel))
    await achannel.send(c.execute('''SELECT cotent FROM messages WHERE channel LIKE 'proto'  and author


                                  ''')

)



bot.run(Discord_TOKEN)


