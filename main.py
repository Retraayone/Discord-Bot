from dotenv import load_dotenv
import discord 
import os
import requests
import json
import random


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

sad_words =["Sad", "sad", "depressed", "unhappy", "angry", 
            "miserable", "depressing", "Depressed",
            "Unhappy", "Angry", "Miserable", "Depressing"]

starter_encouragements = ["Cheer up!",
                        "Hang in there.", 
                        "You are a great person"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data =json.loads(response.text)
    quote = json_data[0]['q'] + "-" + json_data[0]['a']
    return(quote)

    

@client.event
async def on_ready():
    print("We have logged in as{0.user}".format(client))

@client.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))



client.run(os.getenv('TOKEN'))