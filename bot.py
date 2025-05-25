import config
import discord
from discord.ext import commands
import random
import asyncio


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print(f'Kita telah login sebagai {client.user}')

@client.command()
async def about(ctx):
    await ctx.send('Ini adalah echo-bot yang dibuat dengan pustaka discord.py!')

@client.command()
async def command(ctx):
    await ctx.send('belum ada command selain info dan about')

@client.command()
async def explain(ctx):
    if ctx.message.attachments:
        await ctx.send("Thanks for the image! Here's a simple explanation: This is an image you sent.")
    else:
        await ctx.send("Please send an image with your command to explain it.")

@client.event
async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author.id == client.user.id:
            return

        if message.content.startswith('?guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await client.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {answer}.')


client.run(config.TOKEN)
