import os
import discord
from discord.ext import commands
import aiohttp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='h!', intents=intents)

WAIFU_IM_SEARCH_URL = 'https://api.waifu.im/search/'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="🌲linktr.ee/Stying"))
    await bot.tree.sync()
    print(f'We have logged in as {bot.user.name}')

async def fetch_hentai_image(session):
    async with session.get(WAIFU_IM_SEARCH_URL, params={'included_tags': 'hentai'}) as response:
        response.raise_for_status()
        data = await response.json()
        return data

async def fetch_milf_image(session):
    async with session.get(WAIFU_IM_SEARCH_URL, params={'included_tags': 'milf'}) as response:
        response.raise_for_status()
        data = await response.json()
        return data

async def fetch_paizuri_image(session):
    async with session.get(WAIFU_IM_SEARCH_URL, params={'included_tags': 'paizuri'}) as response:
        response.raise_for_status()
        data = await response.json()
        return data

async def fetch_oral_image(session):
    async with session.get(WAIFU_IM_SEARCH_URL, params={'included_tags': 'oral'}) as response:
        response.raise_for_status()
        data = await response.json()
        return data

@bot.hybrid_command(name='hentai', help='Fetch Hentai image or gif')
async def get_hentai_image(ctx):
    try:
        if not ctx.channel.is_nsfw():
            await ctx.send("You can only use the /hentai command in NSFW channels.")
            return

        async with aiohttp.ClientSession() as session:
            data = await fetch_hentai_image(session)

        # Process the API response
        media_list = data.get('images', [])
        if not media_list:
            await ctx.send("No hentai waifu found.")
            return

        # Find the first image or gif URL
        media = next((item for item in media_list if item.get('extension') in ('.jpeg', '.jpg', '.png', '.gif')), None)
        if media is None:
            await ctx.send("No hentai waifu found.")
            return

        media_url = media.get('url')

        # Send just the image or gif URL
        await ctx.send(media_url)

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')

@bot.hybrid_command(name='milf', help='Fetch MILF image or gif')
async def get_milf_image(ctx):
    try:
        if not ctx.channel.is_nsfw():
            await ctx.send("You can only use the /milf command in NSFW channels.")
            return

        async with aiohttp.ClientSession() as session:
            data = await fetch_milf_image(session)

        # Process the API response
        media_list = data.get('images', [])
        if not media_list:
            await ctx.send("No MILF waifu found.")
            return

        # Find the first image or gif URL
        media = next((item for item in media_list if item.get('extension') in ('.jpeg', '.jpg', '.png', '.gif')), None)
        if media is None:
            await ctx.send("No MILF waifu found.")
            return

        media_url = media.get('url')

        # Send just the image or gif URL
        await ctx.send(media_url)

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')

@bot.hybrid_command(name='paizuri', help='Fetch Paizuri image or gif')
async def get_paizuri_image(ctx):
    try:
        if not ctx.channel.is_nsfw():
            await ctx.send("You can only use the /paizuri command in NSFW channels.")
            return

        async with aiohttp.ClientSession() as session:
            data = await fetch_paizuri_image(session)

        # Process the API response
        media_list = data.get('images', [])
        if not media_list:
            await ctx.send("No Paizuri waifu found.")
            return

        # Find the first image or gif URL
        media = next((item for item in media_list if item.get('extension') in ('.jpeg', '.jpg', '.png', '.gif')), None)
        if media is None:
            await ctx.send("No Paizuri waifu found.")
            return

        media_url = media.get('url')

        # Send just the image or gif URL
        await ctx.send(media_url)

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')

@bot.hybrid_command(name='oral', help='Fetch Oral image or gif')
async def get_oral_image(ctx):
    try:
        if not ctx.channel.is_nsfw():
            await ctx.send("You can only use the /oral command in NSFW channels.")
            return

        async with aiohttp.ClientSession() as session:
            data = await fetch_oral_image(session)

        # Process the API response
        media_list = data.get('images', [])
        if not media_list:
            await ctx.send("No Oral waifu found.")
            return

        # Find the first image or gif URL
        media = next((item for item in media_list if item.get('extension') in ('.jpeg', '.jpg', '.png', '.gif')), None)
        if media is None:
            await ctx.send("No Oral waifu found.")
            return

        media_url = media.get('url')

        # Send just the image or gif URL
        await ctx.send(media_url)

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')
try:
    token = os.getenv("TOKEN")
    if token == "":
        raise Exception("Please add your Discord bot token.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
