import disnake.ext.commands
from disnake.ext import commands
from variables.staticData import token
from variables.dynamicData import version

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(","), test_guilds=[913922450205585439], intents=intents)


@bot.event
async def on_ready():
	bot.load_extension(f'base.cogManager')
	print(f"Started with version: {version}")
	await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=''))


@bot.event
async def on_message(message):
	await bot.process_commands(message)


@bot.event
async def on_message_edit(message_before, message_after):
	await bot.process_commands(message_after)


bot.run(token)
