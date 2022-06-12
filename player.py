import urllib
import asyncio
from discord.ext import commands
import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from youtube_dl import YoutubeDL
from asyncio import sleep

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  'options': '-vn'}


bot = commands.Bot(command_prefix='$')

async def on_ready():
    sys.stdout.write('Бот запущен.\Команда: $play <link>')


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
        # ЭТОТ КУСОК КОДА СТОПИТ ТЕКУЩУЮ МУЗЫКУ, ЕСЛИ ВОСПРОИЗВОДИТСЯ, И ВКЛЮЧАЕТ НОВУЮ
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается. Останавливаю, и включаю новую')

        vc.stop()
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))

        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()
        
    else:
        # ЭТОТ КУСОК КОДА ВОСПРОИЗВОДИТ МУЗЫКУ ПО ССЫЛКЕ
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается. Останавливаю, и включаю новую')

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))

        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()

bot.run('OTM4NzUzMjU3OTY1MjI4MDMz.GutY9m.Q-NTIGt3aQ1BKfn35sPuC1arK4by7hiuuzh2tI')
