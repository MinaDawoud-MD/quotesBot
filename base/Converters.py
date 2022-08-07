import disnake
from disnake.ext import commands


class Example(commands.Converter):
	async def convert(self, ctx, argument: str):
		if argument:
			return str(argument)
		raise commands.BadArgument(message='Not a valid test.')


