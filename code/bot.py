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
        data = {'count': 1}
    return data['count']    

@bot.command(name='support')
async def support(ctx):
    ticket_number = await load_ticket_count()
    
    thread = await ctx.channel.create_thread(name=f'Ticket {ticket_number}')
    
    await thread.send(f'How can I help you, {ctx.author.mention}? State your problem please.')
    ticket_number += 1
    await save_ticket_count(ticket_number)

    def check(msg):
        # might change to "thread.channel"
        return msg.author == ctx.author and msg.channel == ctx.channel

    # async def user_response():
    #     user_response = await bot.wait_for('message', check=check, timeout=120)
    #     problem = user_response.content.lower()
    #     return problem
    try:
        # wait for the user, 2 minute timeout
        user_response = await bot.wait_for('message', check=check, timeout=120)

        # turn the user´s input into lowercase for easier processing
        problem = user_response.content.lower()

        # scan the user´s input for keywords and give out possible solutions
        if 'internet' in problem:
            await ctx.send("I see you are having problems with your internet. Have you tried restarting your router?")
        elif 'printer' in problem:
            await ctx.send("Make sure the printer is turned on and properly connected to your computer.")
        elif 'email' in problem:
            await ctx.send("Check your email settings and ensure you have a stable internet connection.")
        elif 'headset' in problem:
            await ctx.send("I see you are having problems with your headset. If it is a USB Headset, check if it is connected to your computer or your dockingstation. If it is a bluetooth headset, check if it is connected and charged (sounds of the headset and lights are good indicators!)")
        else:
            await ctx.send("I'm sorry, I'm not sure how to help with that problem.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond...")

bot.run(Discord_TOKEN)
