import disnake


class Menu(disnake.ui.View):
	"""
	Class for simple left/right Menu view from a list of embeds


	 Attributes
    ----------
    embeds : list[disnake.Embed]
        a list of embeds to show
    """

	def __init__(self, embeds: list[disnake.Embed], author: disnake.Member | None = None, commandMessage: disnake.Message | None = None, startPage: int = 0):
		super().__init__(timeout=None)
		self.embeds = embeds
		self.embed_count = startPage
		self.prev_page.disabled = True if len(self.embeds) <= 1 else False
		self.next_page.disabled = True if len(self.embeds) <= 1 else False
		self.author = author
		self.commandMessage = commandMessage
		for i, embed in enumerate(self.embeds):
			embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")

	@disnake.ui.button(emoji="◀️", style=disnake.ButtonStyle.blurple)  # label="Previous page",
	async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		if self.author is not None and self.author != interaction.author:
			return
		self.embed_count -= 1
		embed = self.embeds[self.embed_count]
		self.next_page.disabled = False
		if self.embed_count == 0:
			self.prev_page.disabled = True
		await interaction.response.edit_message(embed=embed, view=self)

	@disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.green)  # label="Quit",
	async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		if self.author is not None and self.author != interaction.author:
			return
		await interaction.response.edit_message(view=None)
		await interaction.delete_original_message()
		await self.commandMessage.delete()

	@disnake.ui.button(emoji="▶️", style=disnake.ButtonStyle.blurple)  # label="Next page"
	async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		if self.author is not None and self.author != interaction.author:
			return

		self.embed_count += 1
		embed = self.embeds[self.embed_count]

		self.prev_page.disabled = False
		if self.embed_count == len(self.embeds) - 1:
			self.next_page.disabled = True
		await interaction.response.edit_message(embed=embed, view=self)


class DeleteTemplateMenu(disnake.ui.View):
	"""
	Class for simple left/right Menu view from a list of embeds


	 Attributes
    ----------
    embeds : list[disnake.Embed]
        a list of embeds to show
    """

	def __init__(self, embeds: list[disnake.Embed], methodToDelete, initiator):
		super().__init__(timeout=None)
		self.embeds = embeds
		self.embed_count = 0
		self.prev_page.disabled = True
		self.next_page.disabled = True if len(self.embeds) <= 1 else False
		self.remove.disabled = True if len(self.embeds) <= 1 else False
		self.delete_method = methodToDelete
		self.initiator = initiator
		for i, embed in enumerate(self.embeds):
			embed.set_footer(text=f"Template with ID {i + 1} of {len(self.embeds)}")

	@disnake.ui.button(emoji="◀️", style=disnake.ButtonStyle.red)  # label="Previous page",
	async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		if interaction.user != self.initiator:
			return
		self.embed_count -= 1
		embed = self.embeds[self.embed_count]
		self.next_page.disabled = False
		if self.embed_count == 0:
			self.prev_page.disabled = True
		await interaction.response.edit_message(embed=embed, view=self)

	@disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.red)  # label="Quit",
	async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		if interaction.user != self.initiator:
			return
		if len(self.embeds) <= 1:
			self.remove.disabled = True
			return
		self.delete_method(str(interaction.guild.id), self.embed_count)
		await interaction.response.edit_message(view=None)
		await interaction.delete_original_message()

	@disnake.ui.button(emoji="▶️", style=disnake.ButtonStyle.green)  # label="Next page"
	async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		if interaction.user != self.initiator:
			return
		self.embed_count += 1
		embed = self.embeds[self.embed_count]
		self.prev_page.disabled = False
		if self.embed_count == len(self.embeds) - 1:
			self.next_page.disabled = True
		await interaction.response.edit_message(embed=embed, view=self)
