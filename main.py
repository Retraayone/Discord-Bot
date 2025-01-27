from dotenv import load_dotenv
import discord
from discord.ext import commands
import os
import requests
import json
import random

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

sad_words = ["Sad", "sad", "depressed", "unhappy", "angry",
             "miserable", "depressing", "Depressed",
             "Unhappy", "Angry", "Miserable", "Depressing"]

starter_encouragements = ["Cheer up!",
                          "Hang in there.",
                          "You are a great person"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    if message.author == bot.user:
        return

    msg = message.content

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

@bot.slash_command(name="inspire", description="Get an inspirational quote")
async def inspire(ctx):
    quote = get_quote()
    await ctx.respond(quote)

# Get the token from the environment variable
token = os.getenv('TOKEN')
if token is None:
    raise ValueError("No TOKEN environment variable set")

bot.run(token)