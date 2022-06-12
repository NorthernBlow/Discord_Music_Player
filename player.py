import urllib
import asyncio
# import pafy
from discord.ext import commands
import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from youtube_dl import YoutubeDL
from asyncio import sleep

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  'options': '-vn'}

client = discord.Client()

bot = commands.Bot(command_prefix='$')

# 
# ЭТА КОМАНДА ЗАСТАВЛЯЕТ БОТА ПОДКЛЮЧИТЬСЯ К ГОЛОСОВОМУ КАНАЛУ
# 
@bot.command(name='join',aliases = ['summon']) # CREATING COMMAND "JOIN" WITH ALIAS SUMMON
async def _join(ctx, *, channel: discord.VoiceChannel = None): # TAKING ARGUMENT CHANNEL SO PPL CAN MAKE THE BOT JOIN A VOICE CHANNEL THAT THEY ARE NOT IN
    """Joins a voice channel."""

    destination = channel if channel else ctx.author.voice.channel # CHOOSING THE DESTINATION, MIGHT BE THE REQUESTED ONE, BUT IF NOT THEN WE PICK AUTHORS VOICE CHANNEL

    if ctx.voice_client: # CHECKING IF THE BOT IS PLAYING SOMETHING
        await ctx.voice_state.voice.move_to(destination) # IF THE BOT IS PLAYING WE JUST MOVE THE BOT TO THE DESTINATION
        return

    await destination.connect() # CONNECTING TO DESTINATION
    await ctx.send(f"Succesfully joined the voice channel: {destination.name} ({destination.id}).")


# 
# ЭТА КОМАНДА ЗАСТАВЛЯЕТ БОТА ПОДКЛЮЧИТЬСЯ К ГОЛОСОВОМУ КАНАЛУ И ВОСПРОИЗВЕСТИ ЗВУК ИЗ ССЫЛКИ
# 
@bot.command()
async def play(ctx, arg):
    global vc

    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))

        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()

bot.run('your token goes here')
##client.run('OTM4NzUzMjU3OTY1MjI4MDMz.G_W5a6.rouVUtvjOp0h81OVgMiKmP5vaPH7ndzO41Ah6w')
