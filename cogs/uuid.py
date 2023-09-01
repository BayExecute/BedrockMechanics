import uuid, discord, time, datetime
from discord.ext import commands
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

class Uuid(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	@slash.command(name="uuid", description="Generates a UUID",options=[Option("count", "How many uuids you want!", Type.INTEGER)])
	async def get_uuid(self, inter, count: int = 1):
		if count <= 0:
			await inter.reply("Count cant be zero or below!", delete_after = 7)
		elif count > 10:
			await inter.reply("Count cant be over ten!", delete_after = 7)
		else:
			myuuid_list = []
			for x in range(0, count):
				myuuid = uuid.uuid4()
				myuuid_list.append(myuuid)
			else:
				myuuid_str = str(myuuid_list)
				myuuid_str = myuuid_str.replace("'),", "\n\n").replace("UUID('", "").replace("')]", "**").replace("[UUID('", "**").replace("[", "**")
				uuid_embed = discord.Embed(title = "UUID", description = f"Report bugs with **/feedback** if you find any!\n\n```\n{myuuid_str}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
				uuid_embed.set_footer(text=f"Requested in")
				uuid_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
				await inter.reply(embed=uuid_embed)

def setup(Bot):
    Bot.add_cog(Uuid(Bot))
