import re
import discord
import os
from discord.ext import commands
import pafy
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import urllib
import asyncio
import discord
import youtube_dl
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

class music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def dc(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name='test')
    async def test(self, ctx, url):

        if ctx.message.author.voice == None:
            await ctx.send("No Voice Channel")
            return

        channel = ctx.message.author.voice.channel

        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)

        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice_client == None:
            voice_client = await voice.connect()
        else:
            await voice_client.move_to(channel)

        url = url.replace(" ", "+")

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        
        await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])

        song = pafy.new(video_ids[0])  # creates a new pafy object

        audio = song.getbestaudio()  # gets an audio source

        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use

        voice_client.play(source)  # play the source

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

def setup(client):
    client.add_cog(music(client))