import os, discord, asyncio#, string, datetime, time, uuid, dislash, zipfile, json
from discord.ext.commands import cooldown, BucketType
#from zipfile import ZipFile
from discord.ext import commands
from uyan import uyan
from dislash import slash_commands#, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

Bot.load_extension("cogs.data")
Bot.load_extension("cogs.resource")
Bot.load_extension("cogs.feedback")
Bot.load_extension("cogs.uuid")
Bot.load_extension("cogs.addon")
Bot.load_extension("cogs.skin")

#hazırım yazıcı

guilds = [810856253403430944, 727251324252454969, 860199535589457931]
bedrock_mekanik = 860199535589457931
@Bot.event
async def on_ready():
	print("Hazırım! {0.user}".format(Bot))
	Bot.loop.create_task(status_task())
	Bot.loop.create_task(sunucu_kontrol())

async def sunucu_kontrol():
	sunucular = open("sunucular.txt", "w")
	guildler = Bot.guilds
	for guild in guildler:
		isim = guild.name
		isim = f"'{isim}',\n"
		sunucular.write(isim)
	sunucular.close()
	await asyncio.sleep(1200)

async def status_task():
	while True:
		await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Helping crafters on {len(Bot.guilds)} servers!"),status=discord.Status.idle)
		await asyncio.sleep(20)
		await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="/feedback Command is out!"),status=discord.Status.idle)
		await asyncio.sleep(20)

@Bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		cooldown_embed = discord.Embed()
		cooldown_embed.title = "Error!"
		cooldown_embed.color = discord.Color.from_rgb(255, 45, 45)
		cooldown_embed.add_field(name="**Command on cooldown!**", value="**\nTry again after {:.2f}s**".format(error.retry_after))
		await ctx.send(embed=cooldown_embed)

uyan()
Bot.run(os.getenv('TOKEN'))