import discord
import os
import requests
import json
from keep_alive import keep_alive
from discord.ext import commands

import giphy_client
from giphy_client.rest import ApiException
import random

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")


@client.command()
async def ping(ctx):

    await ctx.channel.send(f"Pong {round(client.latency*1000)} ms")


@client.command()
async def gif(ctx, *, q="random"):

    api_key = "Em0y6JhxLKAzcz2aXHs1CPZ78lyECmjA"
    api_instance = giphy_client.DefaultApi()

    try:
        # Search Endpoint

        api_response = api_instance.gifs_search_get(api_key, q, limit=1)
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('.inspire') or (("motivate") in msg.lower()):
        q = get_quote()
        await message.channel.send(q)
    await client.process_commands(message)

    if "HELLO" in msg.upper():
        await message.channel.send(
            f'Hello {message.author.mention} how are you!')
    await client.process_commands(message)


keep_alive()
client.run(os.environ['TOKEN'])
