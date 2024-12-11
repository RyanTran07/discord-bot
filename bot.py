
import discord
import random
from discord import Interaction
from discord.ext import commands
import asyncio
import requests

import sys

import os
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN: str = os.getenv('TOKEN')


bot_intents = discord.Intents.default()
bot_intents.message_content = True

client = commands.Bot(command_prefix = '!', intents = bot_intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("Developers' Guild Project Bot!"))
    print("Bot is ready")

@client.command()
async def ping(ctx):
    print("Ping called")
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def send(ctx, *, userMessage):
    print("Sending message")
    await ctx.send(f'{userMessage}')

@client.command()
async def roll(ctx):
    print("Rolling dice")
    await ctx.send(f'Rolling Dice: {random.randint(1,6)}')

@client.command()
async def coin(ctx):
    print("Flipping coin")
    head = random.randint(1,2);
    if(head == 1):
        await ctx.send('Heads!')
    else:
        await ctx.send('Tails!')

@client.command()
async def remindme(ctx, time:str, *, reminder:str):
    print("Reminder started")
    unit = time[-1]
    if unit not in "smh":
        await ctx.send("Please use a valid unit, 's', 'm', or 'h'")
        return

    time_value = int(time[:-1])
    if unit == "s":
        delay = time_value
    elif unit == "m":
        delay = time_value * 60;
    elif unit == "h":
        delay = time_value * 3600
    else:
        await ctx.send("Invalid unit of time.")
        return

    await ctx.send(f"Reminder has been set! 📅  I'll remind you about {reminder} in {time}.")
    await asyncio.sleep(delay)
    await ctx.send(f"Reminder: {reminder}, {ctx.author.mention}")

@client.command()
async def dog(ctx):
    print("Displaying dog picture")
    req = requests.get("https://dog.ceo/api/breeds/image/random")
    res = req.json()
    embedImage = discord.Embed(title= "🐶")
    embedImage.set_image(url=res['message'])
    await ctx.send(embed=embedImage)

@client.command()
async def rps(ctx, user_choice: str):
    print("Starting Rock Paper Scissors")
    choice_list = ['rock', 'paper', 'scissors']
    random_choice = random.choice(choice_list)
    user_choice = user_choice.lower()

    if user_choice not in choice_list:
        await ctx.send("Invalid choice. Please run the command again and select a valid choice - (Rock 🪨, Paper 📰, Scissors ✂️) ")
        return

    if user_choice == random_choice:
        print("The user and bot have chosen the same rps action.")
        await ctx.send(f"It's a tie! I chose {random_choice}. {ctx.author.mention} chose {user_choice}.")
    elif (user_choice == 'rock' and random_choice == 'scissors') or (user_choice == 'paper' and random_choice == 'rock' ) or (user_choice == 'scissors' and random_choice == 'paper'):
        print("User wins rps.")
        await ctx.send(f'{ctx.author.mention} wins! I chose {random_choice}. {ctx.author.mention} chose {user_choice}. ')
    else:
        print("User lost rps.")
        await ctx.send(f'{ctx.author.mention} loses. I chose {random_choice}. {ctx.author.mention} chose {user_choice}.')

@client.command()
async def commands(ctx):
    print("Commands help called")
    embed_command = discord.Embed(title = "Commands")
    embed_command.add_field(name = "!send [message]", value = "Bot sends your message", inline = False)
    embed_command.add_field(name = "!roll", value = "Rolls a dice from numbers 1 to 6.", inline = False)
    embed_command.add_field(name = "!coin", value = "Performs a coin flip.", inline = False)
    embed_command.add_field(name = "!remindme [length][s, m, h] [task]", value = "Sets a reminder for a task with a timer for the user's desired length (length) and unit of time (seconds, hours, or minutes).", inline = False)
    embed_command.add_field(name = "!dog", value = "Sends a random dog picture.", inline = False)
    embed_command.add_field(name = "!rps [rock, paper, scissors]", value = "Plays rock paper scissors with the bot using the user's choice.", inline = False)
    await ctx.send(embed=embed_command)

client.run(TOKEN)
