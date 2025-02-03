import json

# Load the files
with open("repo/index.json", "r") as f:
    index_data = json.load(f)

with open("repo/assets.json", "r") as f:
    assets_data = json.load(f)

# Create a mapping of filenames to download URLs from assets.json
url_map = {asset["name"]: asset["url"] for asset in assets_data["assets"]}

# Update URLs in index.json data
for item in index_data["data"]:
    filename = item["archive_url"].split("/")[-1]
    if filename in url_map:
        item["archive_url"] = url_map[filename]

# Write updated index.json
with open("index.json", "w") as f:
    json.dump(index_data, f, indent=2)
