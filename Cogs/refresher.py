import discord,asyncio,sqlite3
from Tasks.tasks import embedtask, voicetask, messagetask, playersauto
from Settings.settings import voice
from Scraper.gtcore import GTcore
from discord.ext import commands
from discord.ext.commands import has_permissions
from config import DATABASE_NAME


intents = discord.Intents.all()
client = commands.Bot(command_prefix = "g!", intents = intents)
client.remove_command("help")


class Refresher(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    @commands.is_owner()
    async def tasks(self, ctx):
        print(asyncio.all_tasks())
        await ctx.send(f"```{asyncio.all_tasks()}```")


    @commands.command()
    @has_permissions(administrator = True)
    async def refreshvoice(self, ctx, ip : str):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute(f"SELECT category FROM voice WHERE ip = '{ip}'")
        id = c.fetchone()
        if voice(ip) == True and id is not None:
            category = self.client.get_channel(id[0])
            for channel in category.voice_channels:
                await channel.delete()

            game = GTcore(ip)
            name = game.name()
            map = game.map()
            players = game.players()
            rank = game.rank()

            guild = ctx.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect = False)
            }


            ServerName = await ctx.guild.create_voice_channel(name = name, overwrites = overwrites, category = category)
            Map = await ctx.guild.create_voice_channel(name = f"Map : {map}", overwrites = overwrites, category = category)
            Players = await ctx.guild.create_voice_channel(name=f"Players : {players}", overwrites = overwrites, category = category)
            Rank = await ctx.guild.create_voice_channel(name = f"Rank : {rank}", overwrites = overwrites, category = category)
            Ip = await ctx.guild.create_voice_channel(name = f"Ip : {ip}", overwrites = overwrites, category = category)

            voice_task = self.client.loop.create_task(voicetask(ip, ServerName, Map, Players, Rank, Ip))
            c.execute(f"UPDATE voice SET task = '{voice_task.get_name()}' WHERE guild_id = '{ctx.guild.id}'")
            conn.commit()

            await ctx.send("Voice refresher module has been started.")
        else:
            await ctx.send("First of all use command ``g!voiceauto ip:port``.")


    @refreshvoice.error
    async def refreshvoice_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")


    @commands.command()
    async def refreshembed(self, ctx, id : int):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute(f"SELECT ip FROM users WHERE message_id = '{id}'")
        ip = c.fetchone()
        c.execute(f"SELECT task FROM users WHERE message_id = '{id}'")
        task_name = c.fetchone()
        msg = await ctx.channel.fetch_message(id)

        if task_name is not None:
            _tasks = [tasks for tasks in asyncio.all_tasks() if tasks.get_name() == task_name[0]]

        if ip is not None:
            task = client.loop.create_task(embedtask(ctx.guild.id, ip[0], msg))
            if len(_tasks) != 0:
                _tasks[0].cancel()
            c.execute(f"UPDATE users SET task = '{task.get_name()}' WHERE message_id = '{id}'")
            conn.commit()
            await ctx.send("✅ Module has been started.")
        else:
            await ctx.send("❌ I can't refresh embed.")


    @refreshembed.error
    async def refreshembed_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")


    @commands.command()
    async def refreshmessage(self, ctx, id : int):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute(f"SELECT ip FROM users WHERE message_id = '{id}'")
        ip = c.fetchone()
        c.execute(f"SELECT task FROM users WHERE message_id = '{id}'")
        task_name = c.fetchone()
        msg = await ctx.channel.fetch_message(id)

        if task_name is not None:
            _tasks = [tasks for tasks in asyncio.all_tasks() if tasks.get_name() == task_name[0]]

        if ip is not None:
            task = client.loop.create_task(messagetask(ctx.guild.id, ip[0], msg))
            if len(_tasks) != 0:
                _tasks[0].cancel()
            c.execute(f"UPDATE users SET task = '{task.get_name()}' WHERE message_id = '{id}'")
            conn.commit()
            await ctx.send("✅ Module has been started.")
        else:
            await ctx.send("❌ I can't refresh embed.")

    @refreshmessage.error
    async def refreshmessage_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")


    @commands.command()
    async def refreshplayers(self, ctx, id : int):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute(f"SELECT ip FROM users WHERE message_id = '{id}'")
        ip = c.fetchone()
        c.execute(f"SELECT task FROM users WHERE message_id = '{id}'")
        task_name = c.fetchone()
        msg = await ctx.channel.fetch_message(id)

        if task_name is not None:
            _tasks = [tasks for tasks in asyncio.all_tasks() if tasks.get_name() == task_name[0]]

        if ip is not None:
            task = client.loop.create_task(playersauto(ip[0], msg))
            if len(_tasks) != 0:
                _tasks[0].cancel()
            c.execute(f"UPDATE users SET task = '{task.get_name()}' WHERE message_id = '{id}'")
            conn.commit()
            await ctx.send("✅ Module has been started.")
        else:
            await ctx.send("❌ I can't refresh embed.")

    @refreshplayers.error
    async def refreshplayers_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need ``Administrator`` permission to perfom this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to write ip.")


def setup(client):
    client.add_cog(Refresher(client))