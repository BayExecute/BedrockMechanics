import uuid, discord, time, datetime
from discord.ext import commands
from functions import manifest
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

class Addon(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	@slash.command(name="addon", description="Generates two dependent manifests for addons",options=[Option("bp_name", "Name of the behavior pack manifest", Type.STRING), Option("bp_description", "Description of the behavior pack manifest", Type.STRING), Option("bp_author", "Adds author to the behavior pack manifest (Name1, Name2, Name3...)", Type.STRING), Option("bp_url", "Adds URL to the behavior pack manifest", Type.STRING),Option("rp_name", "Name of the resource pack manifest", Type.STRING), Option("rp_description", "Description of the resource pack manifest", Type.STRING), Option("rp_author", "Adds author to the resource pack manifest (Name1, Name2, Name3...)", Type.STRING), Option("rp_url", "Adds URL to the resource pack manifest", Type.STRING)])
	async def addon(self, inter, bp_name=None, bp_description=None, bp_author=None, bp_url=None, rp_name=None, rp_description=None, rp_author=None, rp_url=None):
		rp_type = "resources"
		rp_pack_id = uuid.uuid4()
		rp_module_id = uuid.uuid4()
		rp_manifest = manifest(rp_name, rp_description, rp_pack_id, rp_module_id, rp_type, rp_author, rp_url)
	
		bp_type = "data"
		bp_pack_id = uuid.uuid4()
		bp_module_id = uuid.uuid4()
		bp_manifest = manifest(bp_name, bp_description, bp_pack_id, bp_module_id, bp_type, bp_author, bp_url, str(rp_pack_id))
	
		dependent_embed = discord.Embed(title = "Addon (dependent) manifest", description = f"Report bugs with **/feedback** if you find any!\n\n**Behavior Pack Manifest**\n```json\n{bp_manifest}\n```\n\n**Resource Pack Manifest**\n```json\n{rp_manifest}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
		dependent_embed.set_footer(text=f"Requested in")
		dependent_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
		await inter.reply(embed=dependent_embed)
def setup(Bot):
    Bot.add_cog(Addon(Bot))
