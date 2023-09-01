import uuid, discord, time, datetime
from discord.ext import commands
from functions import manifest
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

class Resource(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	@slash.command(name="resource", description="Generates a manifest for resource packs", options=[Option("name", "Name of the manifest", Type.STRING),Option("description", "Description of the manifest", Type.STRING),Option("author", "Adds author to manifest", Type.STRING),Option("url", "Adds URL to manifest", Type.STRING)])
	async def rp(self, inter, name=None, description=None, author=None, url=None):
		pack_id = uuid.uuid4()
		module_id = uuid.uuid4()
		pack_type = "resources"
		manifest_text = manifest(name, description, pack_id, module_id, pack_type, author, url)

		rp_embed = discord.Embed(title = "Rescource pack manifest", description = f"Report bugs with **/feedback** if you find any!\n```json\n{manifest_text}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
		rp_embed.set_footer(text=f"Requested in")
		rp_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
		await inter.reply(embed=rp_embed)
def setup(Bot):
    Bot.add_cog(Resource(Bot))
