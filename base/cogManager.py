import disnake
from disnake.ext import commands
from base.embedManager import js2em
from variables.dynamicData import autoStartupCogs


class CogManager(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.loadedCogs = []
		self.loadBaseCogs()

	def loadBaseCogs(self):
		for moduleName in autoStartupCogs:
			self.bot.load_extension(f"cogs.{moduleName}")
			self.loadedCogs.append(moduleName)
		return self.loadedCogs

	def unloadAll(self):
		for moduleName in self.loadedCogs:
			self.bot.unload_extension(f"cogs.{moduleName}")
		returnValue = self.loadedCogs
		self.loadedCogs = []
		return returnValue

	def reloadAll(self):
		for moduleName in self.loadedCogs:
			self.bot.reload_extension(f"cogs.{moduleName}")
		return self.loadedCogs

	@commands.group(name='cog')
	async def _cog(self, ctx):
		# TODO Help commands for groups
		if ctx.invoked_subcommand is None:
			await ctx.channel.send("help soon:tm:")

	@_cog.error
	async def _cog_error(self, ctx, error):
		await ctx.send(embed=js2em.make('error', error=str(error)))

	@commands.is_owner()
	@_cog.command(name='load')
	async def _cog_load(self, ctx: disnake.ext.commands.Context, moduleName: str):
		"""Loads a cog with given module name."""
		if moduleName != 'base':
			self.bot.load_extension(f'cogs.{moduleName}')
			self.loadedCogs.append(moduleName)
			await ctx.send(embed=js2em.make('success', response=f"loaded {moduleName}"))
		else:
			await ctx.send(embed=js2em.make('success', response=f"loaded {self.loadBaseCogs()}"))

	@_cog_load.error
	async def _cog_load_error(self, ctx, error):
		if isinstance(error, commands.ExtensionAlreadyLoaded):
			await ctx.send(embed=js2em.make('error', error=f'Extension {error.name} is already loaded.'))
		elif isinstance(error, commands.CommandInvokeError):
			await ctx.send(embed=js2em.make('error', error=str(error.original).replace("'", "`")))

	@commands.is_owner()
	@_cog.command(name='unload')
	async def _cog_unload(self, ctx: disnake.ext.commands.Context, moduleName: str):
		"""Unloads a cog with given module name or all modules."""
		if moduleName != 'all':
			self.bot.unload_extension(f'cogs.{moduleName}')
			await ctx.send(embed=js2em.make('success', response=f"unloaded {moduleName}"))
			self.loadedCogs.remove(moduleName)
		else:
			await ctx.send(embed=js2em.make('success', response=f"unloaded {self.unloadAll()}"))
			self.loadedCogs = []

	@commands.is_owner()
	@_cog.command(name='reload')
	async def _cog_reload(self, ctx: disnake.ext.commands.Context, moduleName: str):
		"""Reloads a cog with given module name."""
		if moduleName != 'all':
			self.bot.reload_extension(f'cogs.{moduleName}')
			await ctx.send(embed=js2em.make('success', response=f"reloaded {moduleName}"))
		else:
			await ctx.send(embed=js2em.make('success', response=f"reloaded {self.reloadAll()}"))

	@commands.is_owner()
	@_cog.command(name='loaded', aliases=['l'])
	async def _cog_loaded(self, ctx):
		await ctx.send(embed=js2em.make('info', info=str(self.loadedCogs)))


def setup(bot):
	bot.add_cog(CogManager(bot))
