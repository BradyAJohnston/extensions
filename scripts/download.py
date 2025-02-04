import requests
import os
import subprocess


def source_gh_release_info():
    import json

    with open("repo/source.txt", "r") as f:
        lines = f.readlines()

    all_assets = []
    for line in lines:
        command = [
            "gh",
            "release",
            "view",
            "--repo",
            line.strip(),
            "--json",
            "assets,name,url",
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        all_assets.extend(response["assets"])

    with open("repo/assets.json", "w") as f:
        json.dump(all_assets, f, indent=2)


def download_file(url, filename, token=None):
    headers = {"Accept": "application/octet-stream"}
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()

    filepath = os.path.join("repo", filename)
    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return filepath


def main():
    token = os.getenv("GITHUB_TOKEN")

    if not os.path.exists("repo"):
        os.makedirs("repo")

    source_gh_release_info()

    with open("repo/assets.json") as f:
        import json

        assets = json.load(f)

    for asset in assets:
        filepath = os.path.join("repo", asset["name"])
        if os.path.exists(filepath):
            print(f"Skipping:     {asset['name']} (already exists)")
            continue
        print(f"Downloading: {asset['name']}...")
        download_file(asset["url"], asset["name"], token)
        print(f"Done:        {asset['name']}")


if __name__ == "__main__":
    main()
