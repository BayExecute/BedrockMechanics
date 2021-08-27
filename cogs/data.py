import uuid, discord, time, datetime
from discord.ext import commands
from functions import manifest
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

class Data(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	@slash.command(name="data", description="Generates a manifest for behavior packs",options=[Option("name", "Name of the manifest", Type.STRING), Option("description", "Description of the manifest", Type.STRING), Option("author", "Adds author to manifest (Name1, Name2, Name3...)", Type.STRING), Option("url", "Adds URL to manifest", Type.STRING)])
	async def bp(self, inter, name=None, description=None, author=None, url=None):
		pack_id = uuid.uuid4()
		module_id = uuid.uuid4()
		pack_type = "data"
		manifest_text = manifest(name, description, pack_id, module_id, pack_type, author, url)

		bp_embed = discord.Embed(title = "Behavior pack manifest", description = f"```json\n{manifest_text}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
		bp_embed.set_footer(text=f"Requested in")
		bp_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
		await inter.reply(embed=bp_embed)
def setup(Bot):
    Bot.add_cog(Data(Bot))