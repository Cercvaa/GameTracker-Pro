import discord,sqlite3,datetime,pytz,tabulate,asyncio
from discord.ext import commands
from config import DATABASE_NAME, BOT_ID
from discord.ext.commands import has_permissions
from datetime import datetime
from tabulate import tabulate
from pytz import timezone


#import mysql.connector
#Special Modules
from Database.database import Database
from Scraper.gtcore import GTcore
from Tasks.tasks import embedtask, messagetask, voicetask, playersauto

class GameTrackerPro(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def settimezone(self, ctx, time : str):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        try:
            timezone(time)
            c.execute(f"SELECT time FROM timezone WHERE guild_id = '{ctx.guild.id}'")
            result = c.fetchone()
            if result is None:
                c.execute(f"INSERT INTO timezone VALUES('{ctx.guild.id}', '{time}')")
                await ctx.send(f"Timezone set to ``{time}``")
            elif result is not None:
                c.execute(f"UPDATE timezone SET time = '{time}' WHERE guild_id = '{ctx.guild.id}'")
                await ctx.send(f"Timezone updated to ``{time}``")
            conn.commit()
        except pytz.exceptions.UnknownTimeZoneError:
            embed = discord.Embed(title = "❌ Error", description = "**Unknown Timezone, go to the [site](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) and choose correct timezone.**", colour = discord.Colour.red())
            await ctx.send(embed = embed)

    @settimezone.error
    async def settimezone_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")


    @commands.command()
    @has_permissions(administrator = True)
    async def messagelog(self, ctx, channel : discord.TextChannel):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()

        c.execute(f"SELECT channel_id FROM log WHERE guild_id = '{ctx.guild.id}'")
        result = c.fetchone()
        if result is None:
            c.execute(f"INSERT INTO log VALUES('{ctx.guild.id}', '{channel.id}')")
            await ctx.send(f"Log channel set to {channel.mention}")
        elif result is not None:
            c.execute(f"UPDATE log SET channel_id = '{channel.id}' WHERE guild_id = '{ctx.guild.id}'")
            await ctx.send(f"Log channel updated to {channel.mention}")
        conn.commit()

    @messagelog.error
    async def messagelog_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to mention channel.")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()
                                                    #shesacvlelia
        if after.author.bot and before.author.id == BOT_ID and after.content != before.content:
            c.execute(f"SELECT channel_id FROM log WHERE guild_id = '{before.guild.id}'")
            result = c.fetchone()
            if result is None:
                pass
            else:
                channel_id = result[0]
                channel = self.client.get_channel(channel_id)
                embed = discord.Embed(title = "Stats Changed")
                fields = [("Before", before.content, False), ("After", after.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name = name, value = value, inline=inline)

                await channel.send(embed = embed)

    @commands.command()
    @has_permissions(administrator = True)
    async def delip(self, ctx, id : int):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        server = Database(ctx.guild.id)

        c.execute(f"SELECT message_id FROM users WHERE id = '{id}'")
        message = c.fetchone()

        try:
            if server.delip(id) == True:
                msg = await ctx.channel.fetch_message(int(message[0]))
                await msg.delete()
                c.execute(f"DELETE FROM users WHERE id = '{id}'")
                conn.commit()
                await ctx.send(f"{ctx.author.mention}, ID: ``{id}`` removed from database.")
            elif server.delip(id) == False:
                await ctx.send(f"{ctx.author.mention}, ID: ``{id}`` isn't in database.")
        except discord.NotFound:
            c.execute(f"DELETE FROM users WHERE id = '{id}'")
            conn.commit()
            await ctx.send(f"{ctx.author.mention}, ID: ``{id}`` removed from database.")


    @delip.error
    async def delip_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write channel id.")

    @commands.command()
    @has_permissions(administrator = True)
    async def delvoiceip(self, ctx, ip : str):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        server = Database(ctx.guild.id)
        if server.delvcip(ip) == True:
            c.execute(f"DELETE FROM voice WHERE guild_id = '{ctx.guild.id}' AND ip = '{ip}'")
            conn.commit()
            await ctx.send(f"{ctx.author.mention}, Ip: ``{ip}`` deleted from database")
        else:
            await ctx.send(f"❌ {ctx.author.mention}, Ip: ``{ip}`` isn't in database.")

    @delvoiceip.error
    async def delvoiceip_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")

    @commands.command()
    @has_permissions(administrator = True)
    async def dellog(self, ctx, channel : discord.TextChannel):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()

        server = Database(ctx.guild.id)

        if server.delchannel(channel.id) == True:
            c.execute(f"DELETE FROM log WHERE guild_id = '{ctx.guild.id}' AND channel_id = {channel.id}")
            conn.commit()
            await ctx.send(f"{ctx.author.mention}, log channel is deleted.")
        else: await ctx.send(f"{ctx.author.mention}, {channel.mention} is not in this server.")

    @dellog.error
    async def dellog_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgumenFt):
            await ctx.send("You need to mention channel.")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title = "**Help Menu**",
            description = "``g!voiceauto ip:port`` - **The bot will create new voice channels and update them.**\n``g!delvoiceip ip:port`` - **if you want to remove ip from database you can use this command.**\n``g!embedauto ip:port`` - **The bot will create embed and update it.**\n``g!delip channel id`` - **Copy channel id where module is running and use command.**\n``g!messageauto ip:port`` - **The bot will send a message to channel where the command is written.**\n``g!messagelog channel mention``  - **If you are using messageauto module and you want to see changed stats in every 15 minutes use messagelog command.**\n``g!dellog channel id`` - **If you want to delete log channel**\n``g!onlineplayers ip:port`` - **The bot will send message about online players, names, scores and how many hours they are playing. If you want to delete it use g!delip command.**\n``g!settimezone`` - **Set timezone**\n``g!refreshembed message id`` - **Refresh embed module**\n``g!refreshmessage message id`` - **Refresh message module**\n``g!refreshvoice ip:port`` - **Refresh voice module**\n",
            colour = discord.Colour.red()

        )
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(GameTrackerPro(client))