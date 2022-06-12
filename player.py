import urllib
import asyncio
import pafy
from discord.ext import commands
import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from youtube_dl import YoutubeDL
from asyncio import sleep

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  'options': '-vn'}

client = discord.Client()

bot = commands.Bot(command_prefix='$')
# FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}


@bot.command(pass_context=True)
async def SendMessage(self, ctx):
    await ctx.send('Hello')

@bot.command(pass_context=True, name='test')
async def test(self, ctx):
    search = "morpheus tutorials discord bot python"

    if ctx.message.author.voice == None:
        await ctx.send(
            embed=Embeds.txt("No Voice Channel", "You need to be in a voice channel to use this command!", ctx.author))
        return

    channel = ctx.message.author.voice.channel

    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)

    voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

    if voice_client == None:
        voice_client = await voice.connect()
    else:
        await voice_client.move_to(channel)

    search = search.replace(" ", "+")

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])

    song = pafy.new(video_ids[0])  # creates a new pafy object

    audio = song.getbestaudio()  # gets an audio source

    source = FFmpegPCMAudio(audio.url,
                            **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use

    voice_client.play(source)  # play the source

@bot.command(name='join',aliases = ['summon']) # CREATING COMMAND "JOIN" WITH ALIAS SUMMON
async def _join(ctx, *, channel: discord.VoiceChannel = None): # TAKING ARGUMENT CHANNEL SO PPL CAN MAKE THE BOT JOIN A VOICE CHANNEL THAT THEY ARE NOT IN
    """Joins a voice channel."""

    destination = channel if channel else ctx.author.voice.channel # CHOOSING THE DESTINATION, MIGHT BE THE REQUESTED ONE, BUT IF NOT THEN WE PICK AUTHORS VOICE CHANNEL

    if ctx.voice_client: # CHECKING IF THE BOT IS PLAYING SOMETHING
        await ctx.voice_state.voice.move_to(destination) # IF THE BOT IS PLAYING WE JUST MOVE THE BOT TO THE DESTINATION
        return

    await destination.connect() # CONNECTING TO DESTINATION
    await ctx.send(f"Succesfully joined the voice channel: {destination.name} ({destination.id}).")


@bot.command()
async def startq(ctx):
    voicechannel = discord.utils.get(ctx.guild.channels, name='queue')
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio("https://www.youtube.com/watch?v=eFLeZSEKjZ8"), after=lambda e: print('done', e))


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
