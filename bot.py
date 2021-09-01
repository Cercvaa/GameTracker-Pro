import discord,sqlite3
from discord.ext import commands
from config import PREFIX, DATABASE_NAME, TOKEN
from os import environ, listdir
intents = discord.Intents.all()

conn = sqlite3.connect(DATABASE_NAME)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(guild_id TEXT, id TEXT, message_id TEXT, ip TEXT, task TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS voice(guild_id TEXT, ip TEXT, category BIGINT, task TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS log(guild_id TEXT, channel_id INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS timezone(guild_id TEXT, time TEXT)")

client = commands.Bot(command_prefix = PREFIX, intents = intents)
client.remove_command('help')


for cog in filter(lambda x: x.endswith(".py"), listdir("Cogs/")):
    client.load_extension(f"Cogs.{cog[:-3]}")



client.run(TOKEN)
