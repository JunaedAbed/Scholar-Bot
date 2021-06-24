from replit import db
import discord 
import os
import requests
import json
import random
from googlesearch import search 
from keep_alive import keep_alive

my_key = os.environ['TOKEN']

client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']

starter_encouragements = [
    'Cheer Up!', 'Hang in there.', 'You are doing great', 'Everything will be alright fella!'
]

if 'responding' not in db.keys():
    db['responding'] = True

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    data = json.loads(response.text)
    quote = '"' + data[0]['q'] + '"' + " -" + data[0]['a']
    return quote

def get_download(download_content):
    
    paper_url = "https://sci-hub.se/{search_term}".format(search_term=download_content)
    
    return paper_url

def update_encouragements(encouraging_msg):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encouraging_msg)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [encouraging_msg]

def delete_encouragement(index):
    encouragements = db['encouragements']
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements

@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('!please help'):
        response = '`!please inspire --> get random quotes\n!please google --> top 5 google search\n!please new --> add new encouraging words\n!please delete --> delete encouraging words\n!please list --> see the ecouragements list\n!please download --> download article using Sci-hub`'
        await msg.channel.send(response)

    if msg.content.startswith('!please inspire'):
        quote = get_quote()
        await msg.channel.send(quote)

    if db['responding']:
        options = starter_encouragements
        if 'encouragements' in db.keys():
            options.extend(db["encouragements"])

        if any(word in msg.content for word in sad_words):
            await msg.channel.send(random.choice(options))

    if msg.content.startswith('!please new'):
        encouraging_msg = msg.content.split("!please new ", 1)[1]
        update_encouragements(encouraging_msg)
        await msg.channel.send('New encouraging message added!')

    if msg.content.startswith('!please delete'):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.content.split('!please delete', 1)[1])
            delete_encouragement(index)
            encouragements = db['encouragements']
        await msg.channel.send(encouragements.value)

    if msg.content.startswith('!please google'):
        searchContent = ""
        text = str(msg.content).split(' ')
        for i in range(2, len(text)):
            searchContent = searchContent + text[i]

        for j in search(searchContent, tld="co.in", num=5, stop=5, pause=2):
            await msg.channel.send(j)

    if msg.content.startswith('!please list'):
        encouragements = []
        if 'encouragements' in db.keys():
            encouragements = db['encouragements']
        await msg.channel.send(encouragements.value)

    if msg.content.startswith('responding'):
        value = msg.content.split('responding ', 1)[1]

        if value.lower() == 'true':
            db['responding'] = True
            await msg.channel.send("Respoding is on.")
        else: 
            db['responding'] = False
            await msg.channel.send("Respoding is off.")

    if msg.content.startswith('!please download'):
        download_content = ""
        text = str(msg.content).split(' ')
        for i in range(2, len(text)):
            download_content = download_content + text[i]
        download_link = get_download(download_content)
        await msg.channel.send(download_link)

keep_alive()
client.run(my_key)