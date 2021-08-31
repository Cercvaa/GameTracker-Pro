import discord,datetime,asyncio,sqlite3,pytz
from Scraper.gtcore import GTcore
from discord.ext import tasks
from pytz import timezone
from datetime import datetime
from config import *


async def embedtask(guild, ip, message):
    try:
        while True:
            conn = sqlite3.connect(DATABASE_NAME)
            c = conn.cursor()
            
            c.execute(f"SELECT time FROM timezone WHERE guild_id = '{guild}'")
            result = c.fetchone()

            if result is None:
                update = datetime.now().strftime("%m/%d/%Y, %H:%M")
            elif result is not None:
                tz = timezone(result[0])
                update = datetime.now(tz).strftime("%m/%d/%Y, %H:%M")

            server = GTcore(ip)
            name = server.name()    
            map_image = server.mapimage()
            players = server.players()
            rank = server.rank()
            status = server.status()
            map = server.map()

            if map_image == "//image.gametracker.com/images/maps/160x120/nomap.jpg":
                embed = discord.Embed(title = f"```{name}```", colour = discord.Colour.red())
                embed.add_field(name = "<:ip:856091855278964766> Ip :", value = f"``{ip}``")
                embed.add_field(name = "Status :", value = status)
                embed.add_field(name = "🗺️ Map :", value = map)
                embed.add_field(name = "👥 Players :", value = players)
                embed.add_field(name = "🥇 Rank :", value = rank)
                embed.set_footer(text = f"🔄 Last Update: {update}", icon_url = "https://cdn.discordapp.com/avatars/788804106109190154/291662750146799b91c75e793e30fa41.webp")
                await message.edit(embed = embed)
            else:
                embed = discord.Embed(title = f"```{name}```", colour = discord.Colour.red())
                embed.add_field(name = "<:ip:856091855278964766> Ip :", value = f"``{ip}``")
                embed.add_field(name = "Status :", value = status)
                embed.add_field(name = "🗺️ Map :", value = map)
                embed.add_field(name = "👥 Players :", value = players)
                embed.add_field(name = "🥇 Rank :", value = rank)
                embed.set_footer(text = f"🔄 Last Update: {update}", icon_url = "https://cdn.discordapp.com/avatars/788804106109190154/291662750146799b91c75e793e30fa41.webp")
                embed.set_image(url = "https:"+map_image)
                await message.edit(embed = embed)
            

                print("edited")
            await asyncio.sleep(REFRESH_RATE)
    except discord.errors.NotFound:
        print("task is canceled")

async def voicetask(ip, servername : discord.VoiceChannel, map : discord.VoiceChannel, Players : discord.VoiceChannel, Rank : discord.VoiceChannel, Ip : discord.VoiceChannel):
    while True:
        server = GTcore(ip)
        name = server.name()
        map_image = server.map()
        players = server.players()
        rank = server.rank()


        await servername.edit(name = name)
        await map.edit(name = f"Map : {map_image}")
        await Players.edit(name = f"Players : {players}")
        await Rank.edit(name = f"Rank : {rank}")
        await Ip.edit(name = f"Ip : {ip}")
        print("refreshed")
        await asyncio.sleep(REFRESH_RATE)


async def messagetask(guild, ip, message):
    try:
        while True:
            conn = sqlite3.connect(DATABASE_NAME)
            c = conn.cursor()

            c.execute(f"SELECT time FROM timezone WHERE '{guild}'")
            result = c.fetchone()
            if result is not None:
                tz = timezone(result[0])
                update = datetime.now(tz).strftime("%m/%d/%Y, %H:%M")
            elif result is None:
                update = datetime.now().strftime("%m/%d/%Y, %H:%M")
            
            conn.commit()

            server = GTcore(ip)
            map = server.map()
            h = server.name()
            rank = server.rank()
            players = server.players()

            await message.edit(content = f"```Server Name: {h}\n🗺️Map: {map}\n👥Players: {players}\n🥇Rank: {rank}\n🔄Update {update}```")
            await asyncio.sleep(REFRESH_RATE)
    except discord.errors.NotFound:
        print("Task is canceled")

async def playersauto(ip, message):
    try:
        while True:
            server = GTcore(ip)
            tb = server.playersrefresher()

            await message.edit(content = f"```{tb}```")
            await asyncio.sleep(REFRESH_RATE)
    except discord.errors.NotFound:
        print("Task is canceled")
