import discord
from discord.ext import commands
#import ffmpeg lib and i want to show via print() how bitrite is that track

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('my token goes here')
