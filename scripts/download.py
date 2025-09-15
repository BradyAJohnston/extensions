from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

import requests


REPO_DIR = Path("repo")


def source_gh_release_info() -> None:
    import json

    sources_path = REPO_DIR / "source.txt"
    lines: list[str]
    with sources_path.open("r", encoding="utf-8") as f:
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

    assets_path = REPO_DIR / "assets.json"
    with assets_path.open("w", encoding="utf-8") as f:
        json.dump(all_assets, f, indent=2, ensure_ascii=False)


def download_file(url: str, filename: str, token: Optional[str] = None) -> Path:
    headers = {"Accept": "application/octet-stream"}
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(url, headers=headers, stream=True, timeout=60)
    response.raise_for_status()

    filepath = REPO_DIR / filename
    with filepath.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return filepath


def main() -> None:
    import os

    token = os.getenv("GITHUB_TOKEN")

    REPO_DIR.mkdir(parents=True, exist_ok=True)

    source_gh_release_info()

    assets_path = REPO_DIR / "assets.json"
    with assets_path.open("r", encoding="utf-8") as f:
        import json

        assets = json.load(f)

    for asset in assets:
        filepath = REPO_DIR / asset["name"]
        if filepath.exists():
            print(f"Skipping:     {asset['name']} (already exists)")
            continue
        print(f"Downloading: {asset['name']}...")
        download_file(asset["url"], asset["name"], token)
        print(f"Done:        {asset['name']}")


if __name__ == "__main__":
    main()
