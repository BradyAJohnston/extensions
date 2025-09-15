from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlsplit
from typing import Any


REPO_DIR = Path("repo")


def main() -> None:
    index_path = REPO_DIR / "index.json"
    assets_path = REPO_DIR / "assets.json"

    with index_path.open("r", encoding="utf-8") as f:
        index_data: dict[str, Any] = json.load(f)

    with assets_path.open("r", encoding="utf-8") as f:
        assets_data: list[dict[str, Any]] = json.load(f)

    # Create a mapping of filenames to download URLs from assets.json
    url_map = {asset["name"]: asset["url"] for asset in assets_data}

    # Update URLs in index.json data
    for item in index_data["data"]:
        # Extract filename component from URL path
        filename = Path(urlsplit(item["archive_url"]).path).name
        if filename in url_map:
            item["archive_url"] = url_map[filename]

    # Write updated index.json to project root
    out_path = Path("index.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
