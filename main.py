import os
import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

WAIFU_IM_SEARCH_URL = 'https://api.waifu.im/search/'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="🌲linktr.ee/Stying"))
    print(f'We have logged in as {bot.user.name}')

@bot.hybrid_command(name='hentai', help='Fetch Hentai image or gif')
async def get_hentai_image(ctx):
    try:
        if not ctx.channel.is_nsfw():
            await ctx.send("You can only use the !hentai command in NSFW channels.")
            return

        # Define search parameters
        search_params = {
            'included_tags': 'hentai',
        }

        # Make a request to the waifu.im API
        response = requests.get(WAIFU_IM_SEARCH_URL, params=search_params)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors

        # Parse the JSON response
        data = response.json()

        # Extract the first image or gif URL from the array
        media_list = data.get('images', [])
        if not media_list:
            await ctx.send("No hentai waifu found.")
            return

        media = next((item for item in media_list if item.get('extension') in ('.jpeg', '.jpg', '.png', '.gif')), None)
        if media is None:
            await ctx.send("No hentai waifu found.")
            return

        media_url = media.get('url')

        # Create an embed with color #747c8b and footer information
        embed = discord.Embed(color=discord.Color(0x747c8b))
        embed.set_image(url=media_url)
        embed.set_footer(text=f'Requested by {ctx.author.name}')

        # Send the embed to the Discord channel
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')

try:
    token = os.getenv("TOKEN")
    if token == "":
        raise Exception("Please add your Discord bot token to the Secrets pane.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
