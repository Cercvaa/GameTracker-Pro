import discord,asyncio,datetime,sqlite3
from datetime import datetime
from pytz import timezone
from discord.ext import commands
from discord.ext.commands import has_permissions

#Special Modules
from Scraper.gtcore import GTcore
from Tasks.tasks import embedtask, voicetask, messagetask, playersauto
from Database.database import Database
from config import DATABASE_NAME, SERVER_LIMIT


class Module(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(administrator = True)
    async def voiceauto(self, ctx, ip : str):
        server = Database(ctx.guild.id)
        if server.check() == True and server.checkvoiceip(ip) == True:
            conn = sqlite3.connect(DATABASE_NAME)

            game = GTcore(ip)
            name = game.name()
            map = game.map()
            players = game.players()
            rank = game.rank()

            guild = ctx.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect = False)
            }

            category = await guild.create_category("📊 Game Server Stats 📊")
            c = conn.cursor()
            ServerName = await ctx.guild.create_voice_channel(name = name, overwrites = overwrites, category = category)
            Map = await ctx.guild.create_voice_channel(name = f"Map : {map}", overwrites = overwrites, category = category)
            Players = await ctx.guild.create_voice_channel(name=f"Players : {players}", overwrites = overwrites, category = category)
            Rank = await ctx.guild.create_voice_channel(name = f"Rank : {rank}", overwrites = overwrites, category = category)
            Ip = await ctx.guild.create_voice_channel(name = f"Ip : {ip}", overwrites = overwrites, category = category)


            task = self.client.loop.create_task(voicetask(ip, ServerName, Map, Players, Rank, Ip))
            await ctx.send("Voice Channels are created.")
            c.execute(f"INSERT INTO voice VALUES('{ctx.guild.id}', '{ip}', {category.id}, '{task.get_name()}')")
            conn.commit()
        elif server.check() == False:
            await ctx.send(f"The servers limit is {SERVER_LIMIT}.")
        elif server.checkvoiceip(ip) == False:
            await ctx.send(f"``{ip}`` is already running in this channel({ctx.channel.mention}).\n 💡 You can remove ip with this command: ``g!delvoiceip {ip}``")


    @voiceauto.error
    async def voiceauto_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")
    

    @commands.command()
    @has_permissions(administrator = True)
    async def embedauto(self, ctx, ip : str):
        server = Database(ctx.guild.id)
        if server.check() == True and server.fetchid(ip, ctx.channel.id) == False:
            conn = sqlite3.connect(DATABASE_NAME)

            await ctx.channel.purge(limit = 1)
            c = conn.cursor()


            c.execute(f"SELECT time FROM timezone WHERE guild_id = '{ctx.guild.id}'")
            result = c.fetchone()
            if result is None:
                update = datetime.now().strftime("%m/%d/%Y, %H:%M")
            elif result is not None:
                tz = timezone(result[0])
                update = datetime.now(tz).strftime("%m/%d/%Y, %H:%M")

            game = GTcore(ip)
            name = game.name()
            status = game.status()
            map = game.map()
            players = game.players()
            rank = game.rank()
            map_image = game.mapimage()
            if map_image == "//image.gametracker.com/images/maps/160x120/nomap.jpg":
                embed = discord.Embed(title = f"```{name}```", colour = discord.Colour.red())
                embed.add_field(name = "<:ip:856091855278964766> Ip :", value = f"``{ip}``")
                embed.add_field(name = "Status :", value = status)
                embed.add_field(name = "🗺️ Map :", value = map)
                embed.add_field(name = "👥 Players :", value = players)
                embed.add_field(name = "🥇 Rank :", value = rank)
                embed.set_footer(text = f"🔄 Last Update: {update}", icon_url = "https://cdn.discordapp.com/avatars/788804106109190154/291662750146799b91c75e793e30fa41.webp")
                message = await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"```{name}```", colour = discord.Colour.red())
                embed.add_field(name = "<:ip:856091855278964766> Ip :", value = f"``{ip}``")
                embed.add_field(name = "Status :", value = status)
                embed.add_field(name = "🗺️ Map :", value = map)
                embed.add_field(name = "👥 Players :", value = players)
                embed.add_field(name = "🥇 Rank :", value = rank)
                embed.set_footer(text = f"🔄 Last Update: {update}", icon_url = "https://cdn.discordapp.com/avatars/788804106109190154/291662750146799b91c75e793e30fa41.webp")
                embed.set_image(url = "https:"+map_image)
                message = await ctx.send(embed = embed)

            task = self.client.loop.create_task(embedtask(ctx.guild.id, ip, message))
            c.execute(f"INSERT INTO users VALUES('{ctx.guild.id}', '{ctx.channel.id}', '{message.id}', '{ip}', '{task.get_name()}')")
            conn.commit()
            
        elif server.check() == False:
            await ctx.send(f"The servers limit is {SERVER_LIMIT}.")
        elif server.fetchid(ip, ctx.channel.id) == True:
            await ctx.send(f"``{ip}`` is already running in this channel({ctx.channel.mention}).\n 💡 You can remove ip with this command: ``g!delip {ctx.channel.id}``")


    @embedauto.error
    async def embedauto_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")

    @commands.command()
    @has_permissions(administrator = True)
    async def messageauto(self, ctx, ip : str):
        server = Database(ctx.guild.id)
        if server.check() == True and server.fetchid(ip, ctx.channel.id) == False:
            conn = sqlite3.connect(DATABASE_NAME)
            
            c = conn.cursor()
            await ctx.channel.purge(limit = 1)

            game = GTcore(ip)
            name = game.name()
            map = game.map()
            players = game.players()
            rank = game.rank()

            c.execute(f"SELECT time FROM timezone WHERE guild_id = '{ctx.guild.id}'")
            result = c.fetchone()
            if result is not None:
                tz = timezone(result[0])
                update = datetime.now(tz).strftime("%m/%d/%Y, %H:%M")
            elif result is None:
                update = datetime.now().strftime("%m/%d/%Y, %H:%M")

            message = await ctx.send(f"```Server Name: {name}\n🗺️Map: {map}\n👥Players: {players}\n🥇Rank: {rank}\n🔄Last Update: {update}```")
            task = self.client.loop.create_task(messagetask(ctx.guild.id, ip, message))
            c.execute(f"INSERT INTO users VALUES('{ctx.guild.id}', '{ctx.channel.id}', '{message.id}', '{ip}', '{task.get_name()}')")
            conn.commit()
        elif server.check() == False:
            await ctx.send(f"The servers limit is {SERVER_LIMIT}.")
        elif server.fetchid(ip, ctx.channel.id) == True:
            await ctx.send(f"``{ip}`` is already running in this channel({ctx.channel.mention}).\n 💡 You can remove ip with this command: ``g!delip {ctx.channel.id}``")

    @messageauto.error
    async def messageauto_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")


    @commands.command()
    @has_permissions(administrator = True)
    async def onlineplayers(self, ctx, ip : str):
        guild = Database(ctx.guild.id)
        if guild.check() == True and guild.fetchid(ip, ctx.channel.id) == False:
            conn = sqlite3.connect(DATABASE_NAME)
            c = conn.cursor()

            server = GTcore(ip)
            tb = server.playersrefresher()

            message = await ctx.send(f"```{tb}```")
            task = self.client.loop.create_task(playersauto(ip, message))
            c.execute(f"INSERT INTO users VALUES('{ctx.guild.id}', '{ctx.channel.id}', '{message.id}', '{ip}', '{task.get_name()}')")
            conn.commit()
        elif guild.check() == False:
            await ctx.send(f"The servers limit is {SERVER_LIMIT}.")
        elif guild.fetchid(ip, ctx.channel.id) == True:
            await ctx.send(f"``{ip}`` is already running in this channel({ctx.channel.mention}).\n 💡 You can remove ip with this command: ``g!delip {ctx.channel.id}``")

    @onlineplayers.error
    async def onlineplayers_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")

def setup(client):
    client.add_cog(Module(client))