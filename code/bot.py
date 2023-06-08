import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import json 
import sqlite3

# Datenbank erstellen
conn = sqlite3.connect('chat_database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             ticket_name TEXT,
             user_name TEXT,
             problem_message TEXT)''')
# Funktion zum füllen der Datenbank mit Informationen
async def insert_data(ticket_name, user_name, problem_message):
    c.execute("INSERT INTO logs (ticket_name, user_name, problem_message) VALUES (?, ?, ?)",
              (ticket_name, user_name, problem_message))
    conn.commit()
# Beispielfunktion um alle Daten der Datenbank zu ziehen
async def retrieve_data():
    c.execute("SELECT ticket_name, user_name, problem_message FROM logs")
    data = c.fetchall()
    return data
# Funktion zum ziehen der Informationen eines Tickets
async def retrieve_ticket(ticket):
    c.execute(f"SELECT ticket_name, user_name, problem_message FROM logs WHERE ticket_name LIKE '{str(ticket)}'")
    data = c.fetchall()
    return data
# Versteckte Variaben, die man nicht öffentlich im Code zu sehen haben will...
load_dotenv(dotenv_path='./env.env')
Discord_TOKEN = os.getenv('DISCORD_TOKEN')
Discord_TOKEN = str(Discord_TOKEN)
Guild_NAME = os.getenv('GUILD_NAME')
Guild_NAME = str(Guild_NAME)
channel = os.getenv("CHANNEL")
json_path = os.getenv("JSON_PATH")
support_id = os.getenv("SUPPORT_ID")

# Rechte für den Bot
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.messages = True 
bot = commands.Bot(command_prefix='!', intents = intents, privileged_intents=True)

# Login des Bots mit Bestätigung in Konsole sowie Bereitmeldung im Support-Channel
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
    await achannel.send("Heyy! Use !support to get technical help c:")
    
# Speichert die Ticketnummer in einer .json Datei um die aktuellste Ticketnummer auch bei einem Crash zu behalten
async def save_ticket_count(count):
    with open(json_path, 'r') as f:
        data = json.load(f)
    data['count'] = count
    with open(json_path, 'w') as f:
        json.dump(data, f)

# Lädt die aktuelle Ticketnummer aus einer .json Datei
async def load_ticket_count():
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'count': 1}
    return data['count']    

# Bot-Kommando zum auslösen des Chatbots
@bot.command(name='support')
async def support(ctx):
    # thread erstellen und ticketnummer als Threadname nutzen/ticketnummer abspeichern
    ticket_number = await load_ticket_count()
    thread = await ctx.channel.create_thread(name=f'Ticket {ticket_number}')
    await thread.send(f'How can I help you, {ctx.author.mention}? Please state your problem as precise as possible!')
    ticket_number += 1
    await save_ticket_count(ticket_number)

    # check ob die geschickten Nachrichten auch die Nachrichten vom Kommando-Auslöser im Thread kommen und nicht vom Bot selbst
    def check(msg):
        return msg.author == ctx.author and msg.channel == thread
    # ausführen von check()
    async def wait():
        user_response = await bot.wait_for('message', check=check, timeout=600)
        problem = user_response.content.lower()
        return problem

    # selbsterklärend...
    async def closing_thread():
            await thread.send("No response...closing Ticket. Open a new one if needed!")
            await thread.edit(archived=True, locked=True)

     # Keywordbasierte Antworten und Weiterleitung des Problems an menschlichen Support
    try:
        problem = ""
        # Rausziehen und Filtern der Ticketnummer um sie im SQL Select zu nutzen
        async def get_thread_name(thread):
            thread_name = thread.name
            return thread_name
        ticket_name = str(await get_thread_name(thread))
        # filtern der Nummer aus dem Ticket. Beispiel "Ticket 20" wird zu "20"
        async def extract_ticket_number(ticket_string):
            parts = ticket_string.split()
            last_part = parts[-1]
            number = ''.join(filter(str.isdigit, last_part))
            return number
        ticket_number = await extract_ticket_number(ticket_name)

        # nutzen des SQL selects um die Support-Informationen im Thread zu senden
        async def support_information():
            information_list = await retrieve_ticket(ticket_name)
            await thread.send(f"Here are the relevant information for you, Supporter: \n{information_list[0][0]}\nUser: {information_list[0][1]}\nProblem: {information_list[0][2]}")
        # funktion zum hinzufügen der "Supportrolle" in den Thread
        async def request_support():
            await thread.send(f"Hey <@&1115553886627971082> ! {ctx.author.mention} needs some help!")
            await support_information()
        # Auf Antwort des Kunden warten oder Ticket automatisch schließen lassen nach 10min (except case)
        async def autoresolve():
                problem = await wait()
                if problem != None:
                    async def autoresolve_yes_or_no():
                        await thread.send("Do you need Human Support?\nPlease only answer with Yes or No, I will close the ticket if you dont need any more support")
                        problem = await wait()
                        if 'yes' in problem:
                            await request_support()
                        elif 'no' in problem:
                            await thread.send("Alright! Closing ticket!")
                            await closing_thread()
                        else:
                            await thread.send("Please only answer with yes or no...")
                    await autoresolve_yes_or_no()
                else:
                    await thread.send("The issue seems to be solved, I will close the ticket")
                    await closing_thread()  
                    
        # Die verschiedenen Fragen und Antworten getrennt in Internet/Drucker/Email und Headset
        async def internet():
            await thread.send("I see you are having problems with your internet. Have you tried restarting your router?")
            await thread.send("Please only answer with Yes or No")
            problem = await wait()
            if 'yes' in problem:
                await thread.send("Sorry i can not help you anymore. I am requesting support!")
                await request_support() 
                await retrieve_ticket(ticket_name)                   
            elif 'no' in problem:
                await thread.send("Please restart your router and come back for help if you need any!")
                await autoresolve()
            else:
                await thread.send("You did not answer with yes or no...")
                await internet()

        async def printer():
            await thread.send("I see you are having issues with your printer. Which of those Keywords is most accurate for your problem?")
            await thread.send("Ink needed\nconnection problems\n")
            problem = await wait()
            if 'ink' in problem:
                async def ink_yes_or_no():
                    await thread.send("Is some kind of ink missing in the printer?")
                    await thread.send("Please only answer with Yes or No")
                    problem = await wait()
                    if 'yes' in problem:
                        await thread.send("I will request support to order some ink for you")
                        await request_support()
                    elif 'no' in problem:
                        await thread.send("The issue does not seem to be related to ink, i will request some support to help you")
                        await request_support()
                    else:
                        await thread.send("You did not answer with yes or no...")
                        await ink_yes_or_no()
                await ink_yes_or_no()
            elif 'connection' or 'connecting' in problem:
                await thread.send("If you are having issues connecting to the printer, try both restarting your PC and the printer and come back for help if you need any.")
                await autoresolve()
            else:
                await thread.send("It seems like i can not help you here, I am calling for support!")
                await request_support()
        
        async def email():
            await thread.send("I see you are having issues with emailing")
            await thread.send("Do you have issues with sending emails (type 1) or with your Outlook client (type 2)?")
            problem = await wait()
            if '1' in problem:
                await thread.send("Do you have an internet connection?")
                await thread.send("Please only answer with Yes or No")
                problem = await wait()
                if 'yes' in problem:
                    await thread.send("I will request support to help with your problem of sending emails")
                    await request_support()
                elif 'no' in problem:
                    await internet()
                else:
                    await thread.send("You did not answer with yes or no...try again!")
                    await email()
            elif '2' in problem:
                async def client_yes_or_no():
                    await thread.send("Have you tried restarting the Client with the task-manager and/or restarting your computer?")
                    await thread.send("Please only answer with Yes or No")
                    problem = await wait()
                    if 'yes' in problem:
                        await thread.send("I will request some support to help with your client issues")
                        await request_support()
                    elif 'no' in problem:
                        await thread.send("Please restart your client with the Task-Manager and restart your computer if the Task-Manager solution does not work")
                        await autoresolve()
                    else:
                        await thread.send("You did not answer with yes or no...try again!")
                        await client_yes_or_no()
                await client_yes_or_no()
                  
        async def headset():
            await thread.send("I see you are having issues with your headset")
            await thread.send("Do you have a Bluetooth-Headset (type 1) or an USB-Headset (type 2)")
            problem = await wait()
            if '1' in problem:
                async def bluetooth_yes_or_no():
                    await thread.send("Do you have problems connecting your Headset to your pc?")
                    await thread.send("Please only answer with Yes or No")
                    problem = await wait()
                    if 'yes' in problem:
                        await thread.send("I will request some support to help with your headset issues")
                        await request_support()
                    elif 'no' in problem:
                        await thread.send("please connect your headset to your pc")
                        await autoresolve()
                    else:
                        await thread.send("You did not answer with yes or no...try again!")       
                        await bluetooth_yes_or_no()   
                await bluetooth_yes_or_no()                 
            elif '2' in problem:
                async def usb_yes_or_no():
                    await thread.send("Is your Headset connected to your pc?")
                    await thread.send("Please only answer with Yes or No")
                    problem = await wait()
                    if 'yes' in problem:
                        await thread.send("I will request some support to help with your headset issues")
                        await request_support()
                    elif 'no' in problem:
                        await thread.send("please connect your headset to your pc")
                        await autoresolve()
                    else:
                        await thread.send("You did not answer with yes or no...try again!")       
                        await usb_yes_or_no()
                await usb_yes_or_no()  
            else:
                await thread.send("You did not answer with yes or no, try again")
                await headset()
                
        async def chatbot():
            problem = await wait()
            
            # Daten in die Datenbank eingeben
            async for message in thread.history(limit=1):
                problem_message = str(message.content)
            author_name = str(ctx.author)
            await insert_data(ticket_name, author_name, problem_message)
            await retrieve_data()

             # ausführen der Fragen und Antworten
            if 'internet' in problem:
                await internet()
            elif 'wifi' in problem:
                await internet()
            elif 'printer' in problem:
                await printer()
            elif 'printing' in problem:
                await printer()
            elif 'email' in problem:
                await email()
            elif 'headset' in problem:
                await headset()
            else: # Falls der Bot keine Keywords findet, den Nutzer nach relevanten Keywords fragen oder Menschlichen Support rufen
                await thread.send("I have not found any keywords, are one of those topics relevant to your problem? Respond with the respective numbers only please")
                await thread.send("1. Internet/Wifi\n2. Printer/Printing\n3. Email/Emailing\n4. Headset\n5. Call human support")
                problem = await wait()
                if '1' in problem:
                    await internet()
                elif '2' in problem:
                    await printer()
                elif '3' in problem:
                    await email()
                elif '4' in problem:
                    await headset()
                else:
                    await thread.send("Calling for human support!")
                    await request_support()
        await chatbot()

    except asyncio.TimeoutError:
        await thread.send("You took too long to respond... I will close this ticket and you should open a new one")
        await closing_thread()
bot.run(Discord_TOKEN)
