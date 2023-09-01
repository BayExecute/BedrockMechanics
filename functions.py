import json

sample_command = '{"ActorIdentifier":"minecraft:command_block_minecart<>","SaveData":{"Command":"%%command%%","Pos":[],"identifier":"minecraft:command_block_minecart","Ticking":1b,"Persistent":1b},"TicksLeftToStay":0}'

def nbt_command_formatter(commands):
	if commands.strip() == "|" : return None
	else:
		if commands and not commands.strip() == "" or "|" or "None":
			commands = list(str(commands).strip().split("|"))
			for i in range(0, len(commands)-1):
				commands = [i for i in commands if i]
			nbt_commands = []
			for i in commands:
				i = i.replace("/", "").replace(" | ", "").replace(" |", "").replace("| ", "").replace("|", "").strip()
				if i: nbt_commands.append(sample_command.replace('%%command%%', i))
			else:
				if not nbt_commands == []:
					command_string = ""
					for x in nbt_commands:
						if 1 + nbt_commands.index(x) - len(nbt_commands) < 0:
							command_string += x + ",\n"
						else:
							command_string += x
					else:return command_string


def meta_ayarlayici(author, url):
    author_bool = False
    if author and not author.strip() == "" or "," or "None":
        author_bool = True
        author = list(str(author).strip().split(","))
        for i in range(0, len(author)):
            authorstr = str(author[i]).strip()
            author[i] = authorstr
        author = [i for i in author if i]
    url_bool = False
    if not url == None or "":
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


def manifest(name,
             description,
             pack_id,
             module_id,
             pack_type,
             author,
             url,
             dependency: str = None,
             user: str = None,
			 base_game_version: str = None,
			 lock_template_options: str = None):
    if not pack_type == "skin_pack" and name == None or "":
        name = "pack.name"
    elif pack_type == "skin_pack" and name == None or "":
        name = f"{user}'s Skin pack"
    if not pack_type == "skin_pack" and description == None or "":
        description = "pack.description"

    meta = meta_ayarlayici(author, url)

    manifest = {"format_version": 2}
    header = {
        "name": name,
        "description": description,
        "uuid": str(pack_id),
        "version": [1, 0, 0],
        "min_engine_version": [1, 20, 12]
    }
    modules = [{
        "type": pack_type,
        "uuid": str(module_id),
        "version": [1, 0, 0]
    }]
    if pack_type == "skin_pack":
        del header["description"], header["min_engine_version"]
    manifest["header"] = header
    manifest["modules"] = modules

    if dependency:
        dependencies = [{"version": [1, 0, 0], "uuid": dependency}]
        manifest["dependencies"] = dependencies
    if meta and pack_type != "skin_pack":
        manifest["metadata"] = meta

    if base_game_version:
        del header["min_engine_version"]
        manifest["header"]["base_game_version"] = base_game_version
        manifest["header"]["lock_template_options"] = lock_template_options

    manifest = json.dumps(manifest, indent=4, ensure_ascii=False)
    manifest = str(manifest).replace(
        '[\n            1,\n            0,\n            0\n        ]',
        '[ 1, 0, 0 ]'
    ).replace(
        '[\n                1,\n                0,\n                0\n            ]',
        '[ 1, 0, 0 ]'
    ).replace(
        '[\n            1,\n            20,\n            12\n        ]',
        '[ 1, 20, 12 ]')
    manifest = manifest.replace(
        ',\n    "metadata": {\n        "authors": [\n            "None"\n        ]\n    }',
        '')
    return manifest
