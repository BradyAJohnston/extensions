import json
import yaml

with open("repo/index.json", "r") as f:
    data = json.load(f)

info = []

for entry in data["data"]:
    addon_id = entry["id"]
    found = False
    for item in info:
        if item["id"] == addon_id:
            item["platforms"].append(entry["platforms"][0])
            item["archive_urls"].append(entry["archive_url"])
            found = True
            break

    if not found:
        info.append(
            {
                "id": addon_id,
                "title": entry["name"],
                "version": entry["version"],
                "platforms": [entry["platforms"][0]],
                "archive_urls": [entry["archive_url"]],
                "permissions": entry["permissions"],
                "description": entry["tagline"],
                "author": entry["maintainer"],
            }
        )

with open("repo/index.yaml", "w") as f:
    yaml.dump(info, f)
