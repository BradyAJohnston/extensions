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
            item["releases"].append(
                {"platform": entry["platforms"][0], "url": entry["archive_url"]}
            )
            found = True
            break

    if not found:
        info.append(
            {
                "id": addon_id,
                "title": entry["name"],
                "version": entry["version"],
                "releases": [
                    {"platform": entry["platforms"][0], "url": entry["archive_url"]}
                ],
                "website": entry["website"],
                "permissions": entry["permissions"],
                "description": entry["tagline"],
                "maintainer": entry["maintainer"],
                "tagline": entry["tagline"],
                "blender_version_min": entry["blender_version_min"],
                "tags": entry["tags"],
            }
        )

with open("repo/index.yaml", "w") as f:
    yaml.dump(info, f)
