from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def main() -> None:
    with Path("index.json").open("r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    info: list[dict[str, Any]] = []

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

    out_path = Path("repo/index.yaml")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(info, f, allow_unicode=True, sort_keys=False)


if __name__ == "__main__":
    main()
