# Host your own Blender Extensions website

This is an experiment in hosting a [Blender Extensions](https://docs.blender.org/manual/en/latest/advanced/extensions/creating_repository/index.html) website, built via GitHub actions and distributed using GitHub pages and GitHub release downloads for file hosting.

From a simple list of repos to check, all uploaded release assets are found and used to build an `index.json`, which enables a user to subscribe and download extensions from within Blender.

This is intended for distributing development builds of add-ons, or add-ons which don't meet the [rules](https://extensions.blender.org/terms-of-service/) for distribution via the Blender-hosted Extensions platform.

All downloads are just links to the already hosted release files that are available from GitHub repos already, drastically reducing bandwidth requirements for GitHub pages websites.

## Building Locally

Requires a copy of Blender to generate the `index.json`, and [Quarto](https://quarto.org) for static site generation.

To make python environments "just work", I recommend using [`uv`](https://docs.astral.sh/uv/) for any and all package and environment management.

```bash
pip install uv
```

We first download all of the release files from each of the repos defined in `repos/source.txt` using the download script. Then we use Blender to generate the `.json`, then we build the final website using Quarto. I have aliased `blender` to the Blender executable on my system. I recommend you do the samme, but you can also just use the full path to the executable.
```bash
uv run --with requests scripts/download.py
blender --command extension server-generate --repo-dir=repo
uv run --with pyyaml quarto render
```

## Building via GitHub Actions

Using GHA we can automatically build and update the website. The example workflow builds at least once each day, or on every push.

Using `bradyajohnston/setup-blender` we get an installation of Blender aliased to `blender` for our platform. We can then run the independent steps of downloading files, building `index.json` and then building and publishing the site with Quarto.

```yml
name: Download Release Files

on:
  push:
    branches: ["main"]
  schedule:
    - cron: '0 0 * * *'

jobs:
  build-website:
    runs-on: macos-14
    permissions: write-all
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - uses: bradyajohnston/setup-blender@v4
        with: 
          version: latest
      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
            version: "latest"
    
      - name: Get Release Assets
        run: |
          uv run --with requests scripts/download.py
        env:
          GITHUB_TOKEN: ${{ github.token }}
      - name: Generate index.json
        run: |
            blender --command extension server-generate --repo-dir=repo
    
      - name: Quarto Render
        run: |
          uv run --with pyyaml quarto render
    
      - name: Publish to GitHub Pages (and render)
        uses: quarto-dev/quarto-actions/publish@v2
        with:
            target: gh-pages
            path: .
            render: false
        env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
