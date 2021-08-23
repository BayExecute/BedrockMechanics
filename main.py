import os, discord, string, datetime, time, uuid, dislash, zipfile, json, asyncio
from zipfile import ZipFile
from discord.ext import commands
from uyan import uyan
from discord.ext.commands import cooldown, BucketType
from dislash import slash_commands, Option, OptionChoice, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix,help_command=None)
slash = slash_commands.SlashClient(Bot)

#hazırım yazıcı

guilds = [810856253403430944, 727251324252454969, 860199535589457931]
bedrock_mekanik = 860199535589457931
@Bot.event
async def on_ready():
	print("Hazırım! {0.user}".format(Bot))
	Bot.loop.create_task(status_task())

async def status_task():
	while True:
	    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"In a maintance and on {len(Bot.guilds)} servers!"),status=discord.Status.idle)
	    await asyncio.sleep(10)

@Bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		cooldown_embed = discord.Embed()
		cooldown_embed.title = "Error!"
		cooldown_embed.color = discord.Color.from_rgb(255, 45, 45)
		cooldown_embed.add_field(name="**Command on cooldown!**", value="**\nTry again after {:.2f}s**".format(error.retry_after))
		await ctx.send(embed=cooldown_embed)

unicodes = {
	r"\u015f": "ş",
	r"\u015e": "Ş",
	r"\u00e7": "ç",
	r"\u00c7": "Ç",
	r"\u0131": "ı",
	r"\u0130": "İ",
	r"\u00f6": "ö",
	r"\u00d6": "Ö",
	r"\u011f": "ğ",
	r"\u011e": "Ğ",
	r"\u00fc": "ü",
	r"\u00dc": "Ü"
}
unicodes1 = {
	"ş": r"\u015f",
	"Ş": r"\u015e",
	"ç": r"\u00e7",
	"Ç": r"\u00c7",
	"ı": r"\u0131",
	"İ": r"\u0130",
	"ö": r"\u00f6",
	"Ö": r"\u00d6",
	"ğ": r"\u011f",
	"Ğ": r"\u011e",
	"ü": r"\u00fc",
	"Ü": r"\u00dc"
}

#uuid yazıcı
@slash.command(name="uuid", description="Generates a UUID",
options=[
	Option("count", "How many uuids you want!", Type.INTEGER)
	]
)
@commands.cooldown(1, 5, commands.BucketType.user)
async def get_uuid(inter, count: int = 1):
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
			uuid_embed = discord.Embed(title = "UUID", description = f"{myuuid_str}", timestamp = datetime.datetime.utcnow())
			uuid_embed.color = discord.Color.from_rgb(63, 231, 255)
			uuid_embed.set_footer(text=f"Requested in")
			uuid_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
			await inter.reply(embed=uuid_embed)

def meta_ayarlayici(author, url):
	author_bool = False
	if not author == None:
		author_bool = True
		author = list(str(author).strip().split(","))
		for i in range(0, len(author)):
			authorstr = str(author[i]).strip()
			author[i] = authorstr
		author = [i for i in author if i]
	url_bool = False
	if not url == None:
		url_bool = True
	
	meta_list = [url_bool, author_bool]
	meta = False
	if True in meta_list:
		meta = {}
		if author_bool == True:
			meta["authors"] = author
		if url_bool == True:
			meta["url"] = url
		return meta
	else:
		return None

def harf_duzenleyici(manifest):
	manifest = json.dumps(manifest, indent=4)
	manifest = str(manifest).replace('"version": [\n            1,\n            0,\n            0\n        ]', '"version":[ 1, 0, 0 ]').replace('"version": [\n                1,\n                0,\n                0\n            ]', '"version":[ 1, 0, 0 ]').replace('"min_engine_version": [\n            1,\n            13,\n            0\n        ]', '"min_engine_version": [ 1, 13, 0 ]')
	for i in unicodes1:
		for x in unicodes:
			try:
				manifest = manifest.replace(x, i)
			except:
				pass
	return manifest

def manifest(name, description, pack_id, module_id, pack_type, author, url, dependency: str = None, user: str = None):
	if not pack_type == "skin_pack" and name == None:
		name = "pack.name"
	elif pack_type == "skin_pack" and name == None:
		name = f"{user}'s Skin pack"
	if not pack_type == "skin_pack" and description == None:
		description = "pack.description"

	meta = meta_ayarlayici(author, url)
	
	manifest = {"format_version": 2}
	header = {"name": name,"description": description,"uuid": str(pack_id),"version": [ 1, 0, 0 ],"min_engine_version": [ 1, 13, 0 ]}
	modules = [{"type": pack_type,"uuid": str(module_id),"version": [ 1, 0, 0 ]}]
	if pack_type == "skin_pack":
		del header["description"], header["min_engine_version"]
	manifest["header"] = header
	manifest["modules"] = modules

	if dependency:
		dependencies = [ { "version": [ 1, 0, 0 ], "uuid": dependency } ]
		manifest["dependencies"] = dependencies
	if meta and pack_type != "skin_pack":
		manifest["metadata"] = meta

	manifest = harf_duzenleyici(manifest)
	return manifest

#RP manifest yazıcı


@slash.command(name="resource", description="Generates a manifest for resource packs",
options=[
	Option("name", "Name of the manifest", Type.STRING),
	Option("description", "Description of the manifest", Type.STRING),
	Option("author", "Adds author to manifest", Type.STRING),
	Option("url", "Adds URL to manifest", Type.STRING)
	]
)
@commands.cooldown(1, 20, commands.BucketType.user)
async def rp(inter, name=None, description=None, author=None, url=None):
	pack_id = uuid.uuid4()
	module_id = uuid.uuid4()
	pack_type = "resources"
	manifest_text = manifest(name, description, pack_id, module_id, pack_type, author, url)

	rp_embed = discord.Embed(title = "Rescource pack manifest", description = f"```json\n{manifest_text}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
	rp_embed.set_footer(text=f"Requested in")
	rp_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
	await inter.reply(embed=rp_embed)

#BP manifest yazıcı

@slash.command(name="data", description="Generates a manifest for behavior packs",options=[Option("name", "Name of the manifest", Type.STRING), Option("description", "Description of the manifest", Type.STRING), Option("author", "Adds author to manifest (Name1, Name2, Name3...)", Type.STRING), Option("url", "Adds URL to manifest", Type.STRING)])
@commands.cooldown(1, 20, commands.BucketType.user)
async def bp(inter, name=None, description=None, author=None, url=None):
	pack_id = uuid.uuid4()
	module_id = uuid.uuid4()
	pack_type = "data"
	manifest_text = manifest(name, description, pack_id, module_id, pack_type, author, url)

	bp_embed = discord.Embed(title = "Behavior pack manifest", description = f"```json\n{manifest_text}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
	bp_embed.set_footer(text=f"Requested in")
	bp_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
	await inter.reply(embed=bp_embed)


#dependent manifest yazıcı


@slash.command(name="addon", description="Generates two dependent manifests for addons",options=[Option("bp_name", "Name of the behavior pack manifest", Type.STRING), Option("bp_description", "Description of the behavior pack manifest", Type.STRING), Option("bp_author", "Adds author to the behavior pack manifest (Name1, Name2, Name3...)", Type.STRING), Option("bp_url", "Adds URL to the behavior pack manifest", Type.STRING),Option("rp_name", "Name of the resource pack manifest", Type.STRING), Option("rp_description", "Description of the resource pack manifest", Type.STRING), Option("rp_author", "Adds author to the resource pack manifest (Name1, Name2, Name3...)", Type.STRING), Option("rp_url", "Adds URL to the resource pack manifest", Type.STRING)])
@commands.cooldown(1, 20, commands.BucketType.user)
async def addon(inter, bp_name=None, bp_description=None, bp_author=None, bp_url=None, rp_name=None, rp_description=None, rp_author=None, rp_url=None):
	rp_type = "resources"
	rp_pack_id = uuid.uuid4()
	rp_module_id = uuid.uuid4()
	rp_manifest = manifest(rp_name, rp_description, rp_pack_id, rp_module_id, rp_type, rp_author, rp_url)

	bp_type = "data"
	bp_pack_id = uuid.uuid4()
	bp_module_id = uuid.uuid4()
	bp_manifest = manifest(bp_name, bp_description, bp_pack_id, bp_module_id, bp_type, bp_author, bp_url, str(rp_pack_id))

	dependent_embed = discord.Embed(title = "Addon (dependent) manifest", description = f"**Behavior Pack Manifest**\n```json\n{bp_manifest}\n```\n\n**Resource Pack Manifest**\n```json\n{rp_manifest}\n```", color = discord.Color.from_rgb(63, 231, 255), timestamp = datetime.datetime.utcnow())
	dependent_embed.set_footer(text=f"Requested in")
	dependent_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
	await inter.reply(embed=dependent_embed)

@slash.command(name="skin", description="Generates a manifest for skin packs", options=[Option("name", "Name of the manifest", Type.STRING)])
@commands.cooldown(1, 20, commands.BucketType.user)
async def skin(inter, name=None):
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
uyan()
Bot.run(os.getenv('TOKEN'))
