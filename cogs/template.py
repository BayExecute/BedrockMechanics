import uuid, discord, time, datetime
from discord.ext import commands
from functions import manifest
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

class Template(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	@slash.command(name="template", description="Generates a manifest for templates", options=[Option("name", "Name of the manifest", Type.STRING),Option("description", "Description of the manifest", Type.STRING),Option("base_game_version", "Version of the template (1.20.0 | 1.16.100 | etc.)", Type.STRING),Option("lock_template_options", "Toggle for locking template options", Type.STRING, False,
							  choices=[
								  OptionChoice("Lock Template Options", "t"),
								  OptionChoice("Do Not Lock Template Options", "f")
						])])
	async def wt(self, inter, name=None, description=None, author=None, url=None, base_game_version="1.20.12", lock_template_options=True):
		if base_game_version:
			bgv = list(base_game_version.split("."))
			bgvl = []
			can_go = True
			for x in bgv:
				try:
					x = int(x)
					bgvl.append(x)
				except:
					can_go = False
			else:
				if can_go: base_game_version = bgvl
		if can_go:
			if lock_template_options == "t": lock_template_options = True
			if lock_template_options == "f": lock_template_options = False
			pack_id = uuid.uuid4()
			module_id = uuid.uuid4()
			pack_type = "world_template"
			manifest_text = manifest(name, description, pack_id, module_id, pack_type, author, url, base_game_version=base_game_version, lock_template_options=lock_template_options)

			wt_embed = discord.Embed(title = "World Template manifest", description = f"Report bugs with **/feedback** if you find any!\n```json\n{manifest_text}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
			wt_embed.set_footer(text=f"Requested in")
			wt_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
			await inter.reply(embed=wt_embed)
		else:
			wt_embed = discord.Embed(title = "Error", description = f"Input ``{base_game_version}`` is not valid.\nPlease enter the base_template_version like below.\n```\n1.20.12\n1.16.100\netc.```", color = discord.Color.from_rgb(255, 45, 45), timestamp = datetime.datetime.utcnow())
			wt_embed.set_footer(text=f"Requested in")
			wt_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
			await inter.reply(embed=wt_embed, ephemeral=True)
def setup(Bot):
    Bot.add_cog(Template(Bot))
