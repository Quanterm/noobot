import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import json 


load_dotenv(dotenv_path='./env.env')
Discord_TOKEN = os.getenv('DISCORD_TOKEN')
Discord_TOKEN = str(Discord_TOKEN)
Guild_NAME = os.getenv('GUILD_NAME')
Guild_NAME = str(Guild_NAME)
channel = os.getenv("CHANNEL")
json_path = os.getenv("JSON_PATH")
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents = intents, privileged_intents=True)

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
    
    
async def save_ticket_count(count):
    with open(json_path, 'r') as f:
        data = json.load(f)
    data['count'] = count
    with open(json_path, 'w') as f:
        json.dump(data, f)

async def load_ticket_count():
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'count': 0}
    return data['count']    

@bot.command(name='support')
async def support(ctx):
    ticket_number = await load_ticket_count()
    
    thread = await ctx.channel.create_thread(name=f'Ticket {ticket_number}')
    
    await thread.send(f'How can I help you, {ctx.author.mention}?')
    ticket_number += 1
    await save_ticket_count(ticket_number)
bot.run(Discord_TOKEN)
