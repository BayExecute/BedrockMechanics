import uuid, discord, time, datetime, os, zipfile
from discord.ext import commands
from functions import manifest
from zipfile import ZipFile
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

class Data(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	@slash.command(name="skin", description="Generates a manifest for skin packs", options=[Option("name", "Name of the manifest", Type.STRING)])
	async def skin(self, inter, name=None):
		pack_id = uuid.uuid4()
		module_id = uuid.uuid4()

		pack_type = "skin_pack"
		manifest_text = manifest(name, None, pack_id, module_id, pack_type, None, None, None, inter.author.name)
		g = open("skin_pack/manifest.json", "w")
		g.write(manifest_text)
		g.close()

		zipObj = ZipFile('skin_pack/pack.zip', 'w')
		zipObj.write('skin_pack/skins.json')
		zipObj.write('skin_pack/manifest.json')
		zipObj.write('skin_pack/steve.png')
		zipObj.close()

		await inter.reply("Here it is! (this message will destroy itself after 2 minutes!)", delete_after = 120)
		await inter.send(file = discord.File('skin_pack/pack.zip'), delete_after = 120)
		os.remove("skin_pack/pack.zip")
def setup(Bot):
    Bot.add_cog(Data(Bot))