import urllib
import asyncio
import os
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
import discord
from youtube_dl import YoutubeDL
from asyncio import sleep

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Бот запущен и ожидает команду.\nКоманды:\n!play <ссылка> - воспроизводит плейлист\n!kill - убивает бота')


# 
# ЭТА КОМАНДА ВЫЗЫВАЕТ ПОМОЩЬ ПО БОТУ
# 
@bot.command(name='помоги')
async def helpme(ctx):
    await ctx.send(f'Команды:\n!play <ссылка> - воспроизводит плейлист\n!kill - убивает бота\n\nМожно и по русски:\n!включи, !помоги, !умри')


# 
# ЭТА КОМАНДА ЗАСТАВЛЯЕТ БОТА ПОДКЛЮЧИТЬСЯ К ГОЛОСОВОМУ КАНАЛУ И ВОСПРОИЗВЕСТИ ЗВУК ИЗ ССЫЛКИ
# 
@bot.command(name='включи')
async def play(ctx, arg):
    global vc

    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        # ЭТОТ КУСОК КОДА СТОПИТ ТЕКУЩУЮ МУЗЫКУ, ЕСЛИ ВОСПРОИЗВОДИТСЯ, И ВКЛЮЧАЕТ НОВУЮ
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается. Останавливаю, и включаю новую.\nДля воспроизведения другого плейлиста, отправь команду !play <ссылка>')

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
        await ctx.send(f'{ctx.message.author.mention}, включаю музыку.\nДля воспроизведения другого плейлиста, отправь команду !play <ссылка>')

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))

        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()


# 
# ЭТА КОМАНДА ЗАСТАВЛЯЕТ БОТА СЪЕБАТЬСЯ
# 
@bot.command(name='умри')
async def kill(ctx):
    await ctx.send(f'Умер.')
    print('Умер.')
    await ctx.bot.close()


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot.run(environ.get('token'))

if __name__ == '__main__':
    main()
