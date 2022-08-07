import disnake
from disnake.ext import commands


class Example(commands.Cog):
	def __init__(self, bot: disnake.ext.commands.Bot):
		self.bot = bot

	@commands.command(name='example')
	async def example(self, ctx: disnake.ext.commands.Context):
		await ctx.send("Example")


def setup(bot):
	bot.add_cog(Example(bot))
