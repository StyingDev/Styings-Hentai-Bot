import discord
from discord.ext import commands
import aiohttp
import urllib.parse

token = "Your_Discord_token"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='h!', intents=intents)

WAIFU_IM_SEARCH_URL = 'https://api.waifu.im/search/'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="🌲linktr.ee/Stying"))
    await bot.tree.sync()
    print(f'We have logged in as {bot.user.name}')

async def fetch_image(session, tag):
    async with session.get(WAIFU_IM_SEARCH_URL, params={'included_tags': tag}) as response:
        response.raise_for_status()
        return await response.json()

async def send_embed_image(ctx, data, title_prefix):
    media_list = data.get('images', [])
    if not media_list:
        await ctx.send(f"No waifu image found for the requested tag.")
        return

    media = next((item for item in media_list if item.get('extension') in ('.jpeg', '.jpg', '.png', '.gif')), None)
    if media is None:
        await ctx.send(f"No waifu image found for the requested tag.")
        return

    media_url = media.get('url')
    media_extension = urllib.parse.urlparse(media_url).path.split('.')[-1]

    title = f"{title_prefix} {'GIF' if media_extension == 'gif' else 'Image'}"

    embed = discord.Embed(title=title, color=discord.Color(0x747c8b))
    embed.set_image(url=media_url)
    embed.set_footer(text=f'Requested by @{ctx.author.name}')

    await ctx.send(embed=embed)

bot.remove_command("help")

@bot.hybrid_command(name='help', help='Execute for help.')
async def help(ctx):
    embed = discord.Embed(title="Hentai Bot Help", description="Here are the available commands for the hentai Bot:", color=discord.Color(0x747c8b))

    embed.add_field(name="/hentai", value="Fetch Hentai image or gif.", inline=False)
    embed.add_field(name="/milf", value="Fetch MILF image or gif.", inline=False)
    embed.add_field(name="/paizuri", value="Fetch Paizuri image or gif.", inline=False)
    embed.add_field(name="/oral", value="Fetch Oral image or gif.", inline=False)

    await ctx.send(embed=embed)

@bot.hybrid_command(name='hentai', help='Fetch Hentai image or gif')
async def get_hentai_image(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("You can only use the /hentai command in NSFW channels.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            data = await fetch_image(session, 'hentai')

        await send_embed_image(ctx, data, 'Hentai')

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')

@bot.hybrid_command(name='milf', help='Fetch MILF image or gif')
async def get_milf_image(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("You can only use the /milf command in NSFW channels.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            data = await fetch_image(session, 'milf')

        await send_embed_image(ctx, data, 'MILF')

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')

@bot.hybrid_command(name='paizuri', help='Fetch Paizuri image or gif')
async def get_paizuri_image(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("You can only use the /paizuri command in NSFW channels.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            data = await fetch_image(session, 'paizuri')

        await send_embed_image(ctx, data, 'Paizuri')

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')

@bot.hybrid_command(name='oral', help='Fetch Oral image or gif')
async def get_oral_image(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("You can only use the /oral command in NSFW channels.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            data = await fetch_image(session, 'oral')

        await send_embed_image(ctx, data, 'Oral')

    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')


bot.run(token)
