import disnake
import json
from datetime import datetime


def make(name: str, category: str = 'system', **kwargs):
	if category == 'system':
		fp = 'base/embedManager/embeds/embeds.json'
	else:
		fp = f'cogs/{category}/embeds.json'

	with open(fp, encoding='utf-8') as f:
		fullData = json.load(f)
	data = fullData[name]['embeds'][0]

	for key in data:
		for pkey in kwargs:
			if type(data[key]) == str:
				data[key] = data[key].replace('{$' + pkey + '}', kwargs[pkey])
			elif type(data[key]) == dict:
				for nKey in data[key]:
					data[key][nKey] = data[key][nKey].replace('{$' + pkey + '}', kwargs[pkey])

	def checkEntryExists(name, data):
		if name in data:
			return len(name) > 0
		return False

	embed = disnake.Embed(
		title=str(data["title"]) if checkEntryExists("title", data) else "",
		description=str(data["description"])
		if checkEntryExists("description", data)
		else "",
		color=int(data["color"]) if data['color'] is not None else 2895667
		if checkEntryExists("color", data)
		else 2895667,
		url=str(data["url"]) if checkEntryExists("url", data) else "",
	)

	if checkEntryExists("fields", data):
		for field in data["fields"]:
			embed.add_field(
				name=str(field["name"]) if checkEntryExists("name", field) else "",
				value=str(field["value"])
				if checkEntryExists("value", field)
				else "",
				inline=bool(field["inline"])
				if checkEntryExists("inline", field)
				else False,
			)
	if checkEntryExists("author", data):
		embed.set_author(
			name=str(data["author"]["name"])
			if checkEntryExists("name", data["author"])
			else "",
			url=str(data["author"]["url"])
			if checkEntryExists("url", data["author"])
			else "",
			icon_url=str(data["author"]["icon_url"])
			if checkEntryExists("icon_url", data["author"])
			else "",
		)

	if checkEntryExists("thumbnail", data):
		embed.set_thumbnail(
			url=str(data["thumbnail"]["url"])
			if checkEntryExists("url", data["thumbnail"])
			else "",
		)

	if checkEntryExists("timestamp", data):
		embed.timestamp = datetime.fromisoformat(str(data["timestamp"])[:-1]) if checkEntryExists("timestamp",
		                                                                                          data) else ""

	if checkEntryExists("image", data):
		embed.set_image(
			url=str(data["image"]["url"])
			if checkEntryExists("url", data["image"])
			else "",
		)

	if checkEntryExists("footer", data):
		embed.set_footer(
			text=str(data["footer"]["text"])
			if checkEntryExists("text", data["footer"])
			else "",
			icon_url=str(data["footer"]["icon_url"])
			if checkEntryExists("icon_url", data["footer"])
			else "",
		)

	return embed
