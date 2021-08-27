import json
unicodes = { r"\u015f": "ş", r"\u015e": "Ş", r"\u00e7": "ç", r"\u00c7": "Ç", r"\u0131": "ı", r"\u0130": "İ", r"\u00f6": "ö", r"\u00d6": "Ö", r"\u011f": "ğ", r"\u011e": "Ğ", r"\u00fc": "ü", r"\u00dc": "Ü" }
unicodes1 = { "ş": r"\u015f", "Ş": r"\u015e", "ç": r"\u00e7", "Ç": r"\u00c7", "ı": r"\u0131", "İ": r"\u0130", "ö": r"\u00f6", "Ö": r"\u00d6", "ğ": r"\u011f", "Ğ": r"\u011e", "ü": r"\u00fc", "Ü": r"\u00dc" }

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