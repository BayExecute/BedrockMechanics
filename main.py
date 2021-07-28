import os, discord, string, datetime, time, uuid, dislash, zipfile
from zipfile import ZipFile
from discord.ext import commands
from discord import Client
from uyan import uyan
from discord.ext.commands import cooldown, BucketType
from dislash import *
from dislash.interactions import *

# skin_pack_json = open("jsons/skin_pack/manifest.json", "r")
# print(skin_pack_json.read())
# skin_pack_json.close()

meta_full = '{}{}{}{}{}'

meta_not_full = '{}{}{}'

pack_meta_part1 = '{'
pack_meta_part2 = '\n		"authors": {}'
pack_meta_part3 = ','
pack_meta_part4 = '\n		"url": "{}"'
pack_meta_part5 ='\n	}'

activity = discord.Game(name='"/help" for Help!')

# zipObj = ZipFile('sample.mcaddon', 'w')
# zipObj.write('sample_file.csv')
# zipObj.write('test_1.log')
# zipObj.write('test_2.log')
# zipObj.close()

#intents
prefix = "?"
Bot = commands.Bot(command_prefix=prefix,activity=activity,status=discord.Status.idle,help_command=None)
slash = slash_commands.SlashClient(Bot)

#hazırım yazıcı

guilds = [810856253403430944, 727251324252454969, 860199535589457931]
bedrock_mekanik = 860199535589457931
@Bot.event
async def on_ready():
	print("Hazırım! {0.user}".format(Bot))

@Bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		cooldown_embed = discord.Embed()
		cooldown_embed.title = "Error!"
		cooldown_embed.color = discord.Color.from_rgb(255, 45, 45)
		cooldown_embed.add_field(name="**Command on cooldown!**", value="**\nTry again after {:.2f}s**".format(error.retry_after))
		await ctx.send(embed=cooldown_embed)

#uuid yazıcı
@slash.command(name="uuid", description="Generates a UUID",
options=[
	Option("count", "How many uuids you want!", Type.INTEGER)
	]
)
@commands.cooldown(1, 5, commands.BucketType.user)
async def get_uuid(inter, count: int = 1):
	uuid_embed = discord.Embed()
	uuid_embed.color = discord.Color.from_rgb(63, 231, 255)
	uuid_embed.title = "UUID"
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
			uuid_embed.description = f"{myuuid_str}"
			uuid_embed.set_footer(text=f"Requested in")
			uuid_embed.timestamp = datetime.datetime.utcnow()
			uuid_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
			await inter.reply(embed=uuid_embed)


#uuid yazıcı


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
	if name == None:
		name = "pack.name"
	else:
		pass

	if description == None:
		description = "pack.description"
	else:
		pass

	if not author == None:
		author_bool = True
	else:
		author_bool = False

	if not url == None:
		url_bool = True
	else:
		url_bool = False

	if author_bool == True and url_bool == True:
		author = author.strip().split(", " and ",")
		meta = meta_full.format(pack_meta_part1, pack_meta_part2.format(author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part3, pack_meta_part4.format(url), pack_meta_part5)
	elif author_bool == True and url_bool == False:
		author = author.strip().split(", " and ",")
		meta = meta_not_full.format(pack_meta_part1, pack_meta_part2.format(author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part5)
	elif author_bool == False and url_bool == True:
		meta = meta_not_full.format(pack_meta_part1, pack_meta_part4.format(url), pack_meta_part5)
	else:
		meta = None

	pack_id = uuid.uuid4()
	module_id = uuid.uuid4()

	pack_type = "resources"
	rp_embed = discord.Embed()
	rp_embed.title = "Resource pack manifest"
	rp_embed.color = discord.Color.from_rgb(63, 231, 255)
	rp_embed.set_footer(text=f"Requested in")
	rp_embed.timestamp = datetime.datetime.utcnow()
	rp_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
	if meta == None:
		doc_manifest = open("manifest_templates/non_dependent.txt", "r")
		manifest = str(doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		manifest = manifest.replace('şn', name).replace('şd', description).replace('şu1', f"{pack_id}").replace('şt', pack_type).replace('şu2', f"{module_id}")
		manifest = manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		rp_embed.description = f"```json\n{manifest}\n```"
		doc_manifest.close()
	else:
		doc_manifest = open("manifest_templates/non_dependent_meta.txt", "r")
		manifest = str(doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		manifest = manifest.replace('şn', name).replace('şd', description).replace('şu1', f"{pack_id}").replace('şt', pack_type).replace('şu2', f"{module_id}").replace('şm', meta)
		manifest = manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		rp_embed.description = f"```json\n{manifest}\n```"
		doc_manifest.close()
	await inter.reply(embed=rp_embed)

#BP manifest yazıcı

@slash.command(name="data", description="Generates a manifest for behavior packs",options=[Option("name", "Name of the manifest", Type.STRING), Option("description", "Description of the manifest", Type.STRING), Option("author", "Adds author to manifest (Name1, Name2, Name3...)", Type.STRING), Option("url", "Adds URL to manifest", Type.STRING)])
@commands.cooldown(1, 20, commands.BucketType.user)
async def bp(inter, name=None, description=None, author=None, url=None):
	if name == None:
		name = "pack.name"
	else:
		pass

	if description == None:
		description = "pack.description"
	else:
		pass

	if not author == None:
		author_bool = True
	else:
		author_bool = False

	if not url == None:
		url_bool = True
	else:
		url_bool = False

	if author_bool == True and url_bool == True:
		author = author.strip().split(", " and ",")
		meta = meta_full.format(pack_meta_part1, pack_meta_part2.format(author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part3, pack_meta_part4.format(url), pack_meta_part5)
	elif author_bool == True and url_bool == False:
		author = author.strip().split(", " and ",")
		meta = meta_not_full.format(pack_meta_part1, pack_meta_part2.format(author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part5)
	elif author_bool == False and url_bool == True:
		meta = meta_not_full.format(pack_meta_part1, pack_meta_part4.format(url), pack_meta_part5)
	else:
		meta = None

	pack_id = uuid.uuid4()
	module_id = uuid.uuid4()

	pack_type = "data"
	bp_embed = discord.Embed()
	bp_embed.title = "Behavior pack manifest"
	bp_embed.color = discord.Color.from_rgb(63, 231, 255)
	bp_embed.set_footer(text=f"Requested in")
	bp_embed.timestamp = datetime.datetime.utcnow()
	bp_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
	if meta == None:
		doc_manifest = open("manifest_templates/non_dependent.txt", "r")
		manifest = str(doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		manifest = manifest.replace('şn', name).replace('şd', description).replace('şu1', f"{pack_id}").replace('şt', pack_type).replace('şu2', f"{module_id}")
		manifest = manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		bp_embed.description = f"```json\n{manifest}\n```"
		doc_manifest.close()
	else:
		doc_manifest = open("manifest_templates/non_dependent_meta.txt", "r")
		manifest = str(doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		manifest = manifest.replace('şn', name).replace('şd', description).replace('şu1', f"{pack_id}").replace('şt', pack_type).replace('şu2', f"{module_id}").replace('şm', meta)
		manifest = manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		bp_embed.description = f"```json\n{manifest}\n```"
		doc_manifest.close()
	await inter.reply(embed=bp_embed)


#dependent manifest yazıcı


@slash.command(name="addon", description="Generates two dependent manifests for addons",options=[Option("bp_name", "Name of the behavior pack manifest", Type.STRING), Option("bp_description", "Description of the behavior pack manifest", Type.STRING), Option("bp_author", "Adds author to the behavior pack manifest (Name1, Name2, Name3...)", Type.STRING), Option("bp_url", "Adds URL to the behavior pack manifest", Type.STRING),Option("rp_name", "Name of the resource pack manifest", Type.STRING), Option("rp_description", "Description of the resource pack manifest", Type.STRING), Option("rp_author", "Adds author to the resource pack manifest (Name1, Name2, Name3...)", Type.STRING), Option("rp_url", "Adds URL to the resource pack manifest", Type.STRING)])
@commands.cooldown(1, 20, commands.BucketType.user)
async def addon(inter, bp_name=None, bp_description=None, bp_author=None, bp_url=None, rp_name=None, rp_description=None, rp_author=None, rp_url=None):
	if bp_name == None:
		bp_name = "pack.name"
	else:
		pass

	if bp_description == None:
		bp_description = "pack.description"
	else:
		pass

	if not bp_author == None:
		bp_author_bool = True
	else:
		bp_author_bool = False

	if not bp_url == None:
		bp_url_bool = True
	else:
		bp_url_bool = False

	if bp_author_bool == True and bp_url_bool == True:
		bp_author = bp_author.strip().split(", " and ",")
		bp_meta = meta_full.format(pack_meta_part1, pack_meta_part2.format(bp_author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part3, pack_meta_part4.format(bp_url), pack_meta_part5)
	elif bp_author_bool == True and bp_url_bool == False:
		bp_author = bp_author.strip().split(", " and ",")
		bp_meta = meta_not_full.format(pack_meta_part1, pack_meta_part2.format(bp_author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part5)
	elif bp_author_bool == False and bp_url_bool == True:
		bp_meta = meta_not_full.format(pack_meta_part1, pack_meta_part4.format(bp_url), pack_meta_part5)
	else:
		bp_meta = None

	if rp_name == None:
		rp_name = "pack.name"
	else:
		pass

	if rp_description == None:
		rp_description = "pack.description"
	else:
		pass

	if not rp_author == None:
		rp_author_bool = True
	else:
		rp_author_bool = False

	if not rp_url == None:
		rp_url_bool = True
	else:
		rp_url_bool = False

	if rp_author_bool == True and rp_url_bool == True:
		rp_author = rp_author.strip().split(", " and ",")
		rp_meta = meta_full.format(pack_meta_part1, pack_meta_part2.format(rp_author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part3, pack_meta_part4.format(rp_url), pack_meta_part5)
	elif rp_author_bool == True and rp_url_bool == False:
		rp_author = rp_author.strip().split(", " and ",")
		rp_meta = meta_not_full.format(pack_meta_part1, pack_meta_part2.format(rp_author).replace("' ",'"').replace("'",'"').replace("',",'",').replace('["', '[\n          "').replace(', "', ',\n          "').replace('"]', '"\n        ]'), pack_meta_part5)
	elif rp_author_bool == False and rp_url_bool == True:
		rp_meta = meta_not_full.format(pack_meta_part1, pack_meta_part4.format(rp_url), pack_meta_part5)
	else:
		rp_meta = None

	rp_pack_id = uuid.uuid4()
	rp_module_id = uuid.uuid4()

	bp_pack_id = uuid.uuid4()
	bp_module_id = uuid.uuid4()

	bp_pack_type = "data"
	rp_pack_type = "resources"

	dependent_embed = discord.Embed()
	dependent_embed.title = "Addon (dependent) manifest"
	dependent_embed.color = discord.Color.from_rgb(63, 231, 255)
	dependent_embed.set_footer(text=f"Requested in")
	dependent_embed.timestamp = datetime.datetime.utcnow()
	dependent_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)

	if bp_meta == None:
		bp_doc_manifest = open("manifest_templates/dependent.txt", "r")
		bp_manifest = str(bp_doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		bp_manifest = bp_manifest.replace('bşn', bp_name).replace('bşd', bp_description).replace('bşu1', f"{bp_pack_id}").replace('bşt', bp_pack_type).replace('bşu2', f"{bp_module_id}").replace('rşu2', f"{rp_module_id}")
		bp_manifest = bp_manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		bp = f"```json\n{bp_manifest}\n```"
		bp_doc_manifest.close()
	else:
		bp_doc_manifest = open("manifest_templates/dependent_meta.txt", "r")
		bp_manifest = str(bp_doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		bp_manifest = bp_manifest.replace('bşn', bp_name).replace('bşd', bp_description).replace('bşu1', f"{bp_pack_id}").replace('bşt', bp_pack_type).replace('bşu2', f"{bp_module_id}").replace('rşu2', f"{rp_module_id}").replace('bşm', bp_meta)
		bp_manifest = bp_manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		bp = f"**Behavior Pack**\n```json\n{bp_manifest}\n```"
		bp_doc_manifest.close()
	if rp_meta == None:
		rp_doc_manifest = open("manifest_templates/non_dependent.txt", "r")
		rp_manifest = str(rp_doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		rp_manifest = rp_manifest.replace('şn', rp_name).replace('şd', rp_description).replace('şu1', f"{rp_pack_id}").replace('şt', rp_pack_type).replace('şu2', f"{rp_module_id}")
		rp_manifest = rp_manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		rp = f"**Resource Pack**\n```json\n{rp_manifest}\n```"
		rp_doc_manifest.close()
	else:
		rp_doc_manifest = open("manifest_templates/non_dependent_meta.txt", "r")
		rp_manifest = str(rp_doc_manifest.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
		rp_manifest = rp_manifest.replace('şn', rp_name).replace('şd', rp_description).replace('şu1', f"{rp_pack_id}").replace('şt', rp_pack_type).replace('şu2', f"{rp_module_id}").replace('şm', rp_meta)
		rp_manifest = rp_manifest.replace("ş5", "\n					").replace("ş4", "\n				").replace("ş3", "\n			").replace("ş2","\n		").replace("ş1", "\n	").replace("ş0", "\n")
		rp = f"**Resource Pack**\n```json\n{rp_manifest}\n```"
		rp_doc_manifest.close()
	dependent_embed.description = f"{bp}\n{rp}"
	await inter.reply(embed=dependent_embed)



@slash.command(name="skin", description="Generates a manifest for skin packs", options=[Option("name", "Name of the manifest", Type.STRING, True)])
@commands.cooldown(1, 20, commands.BucketType.user)
async def skin(inter, name=None):
	pack_id = uuid.uuid4()
	module_id = uuid.uuid4()

	pack_type = "skin_pack"
	skin_embed = discord.Embed()
	skin_embed.title = "Skin pack manifest"
	skin_embed.color = discord.Color.from_rgb(63, 231, 255)
	skin_temp = open("manifest_templates/skin_pack.txt", "r")
	skin_temp_str = str(skin_temp.read()).replace("\n					", "ş5").replace("\n				", "ş4").replace("\n			", "ş3").replace("\n		", "ş2").replace("\n	", "ş1").replace("\n", "ş0")
	
	skin_embed.description = manifest_skin.format(pack_part1, pack_part2, pack_part3, pack_part4.format(name), pack_part6.format(pack_id), pack_part7, pack_part9, pack_part10, pack_part11, pack_part12.format(pack_type), pack_part13.format(module_id), pack_part14, pack_part15, pack_part16, pack_part17)
	skin_embed.set_footer(text=f"Requested in")
	skin_embed.timestamp = datetime.datetime.utcnow()
	skin_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
	await inter.reply(embed=skin_embed)


@slash.command(name="help", description="Shows all commands!", options = [
	Option("command", "Choose one if you looking for specific help!", Type.STRING, False, choices=[
            OptionChoice("/uuid", "/uuid"),
            OptionChoice("/resource", "/resource"),
            OptionChoice("/data", "/data"),
            OptionChoice("/skin", "/skin"),
            OptionChoice("/addon", "/addon")
        	]
		)
	]
)
#help
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(inter, command = None):

	if command == None:
		command = 0
	elif command == "/uuid":
		command = 1
	elif command == "/resource":
		command = 2
	elif command == "/data":
		command = 3
	elif command == "/skin":
		command = 4
	elif command == "/addon":
		command = 5
	else:
		await inter.reply("Please put a valid argument!")

	if command == 0:
		help_embed = discord.Embed(title="Commands List")
		help_embed.add_field(name="→ /uuid", value="Generates a uuid.", inline=False)
		help_embed.add_field(name="→ /resource", value="Generates a manifest for resource packs.", inline=False)
		help_embed.add_field(name="→ /data", value="Generates a manifest for behavior packs.", inline=False)
		help_embed.add_field(name="→ /skin", value="Generates a manifest for skin packs.", inline=False)
		help_embed.add_field(name="→ /addon", value="Generates two manifests connected each other.", inline=False)
	elif command == 1:
		help_embed = discord.Embed(title="→ /uuid")
		help_embed.description = "**Generates a random uuid.\n\nInputs:\n> This command doesnt get any inputs**"
		help_embed.set_footer(text = "Thanks to uuidgenerator.net for api")
	elif command == 2:
		help_embed = discord.Embed(title="→ /resource")
		help_embed.description = "**Generates a resource pack manifest.\n\nInputs:\n> Name: Text, e.g.(Powerfull Pack of Mine)\n\n> Description: Text, e.g.(Gives a powerfull feeling when used!)\n\n> Author: List, e.g.(BayExecute, Manifest Bot, etc)\n\n> URL:Text, e.g.(bayexecute.xyz)**"
	elif command == 3:
		help_embed = discord.Embed(title="→ /data")
		help_embed.description = "**Generates a behavior pack manifest.\n\nInputs:\n> Name: Text, e.g.(Powerfull Pack of Mine)\n\n> Description: Text, e.g.(Gives a powerfull feeling when used!)\n\n> Author: List, e.g.(BayExecute, Manifest Bot, etc)\n\n> URL:Text, e.g.(bayexecute.xyz)**"
	elif command == 4:
		help_embed = discord.Embed(title="→ /skin")
		help_embed.description = "**Generates a skin pack manifest.\n\nInputs:**\n> Name: Text, e.g.(Powerfull Pack of Mine), Not Optional!"
	elif command == 5:
		help_embed = discord.Embed(title="→ /addon")
		help_embed.description = "**Generates two dependent manifests for addons.\n\nInputs For:\nBehavior pack\n\n> Name: Text, e.g.(Powerfull BP of Mine)\n\n> Description: Text, e.g.(Gives a powerfull feeling when used!)\n\n> Author: List, e.g.(BayExecute, Manifest Bot, etc)\n\n> URL:Text, e.g.(bayexecute.xyz)\n\nResource pack\n\n> Name: Text, e.g.(Powerfull RP of Mine)\n\n> Description: Text, e.g.(Gives a powerfull feeling when used!)\n\n> Author: List, e.g.(BayExecute, Manifest Bot, etc)\n\n> URL:Text, e.g.(bayexecute.xyz)**"
	if not help_embed.description == None:
		help_embed.color = discord.Color.from_rgb(63, 231, 255)
		help_embed.set_footer(text=f"Requested in")
		help_embed.timestamp = datetime.datetime.utcnow()
		help_embed.set_author(name=f"{inter.author.name}#{inter.author.discriminator}", icon_url=inter.author.avatar_url)
		await inter.reply(embed=help_embed)
	else:
		pass

uyan()
Bot.run(os.getenv('TOKEN'))