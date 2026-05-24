#!/usr/bin/env python3
"""Regenerates the PROJECTS-START…PROJECTS-END block in README.md.
Omits the star badge entirely when a repo has 0 stars."""

import json
import re
import subprocess

OWNER = "PolskiGlizda"

PROJECTS = [
    ("C",          "GShell",      "POSIX-compatible shell written from scratch — zero external deps"),
    ("TypeScript", "FormFiller",  "Automated Google Forms filler with a randomizing TUI"),
    ("Go",         "calculator",  "Terminal calculator with braille plots & live syntax highlighting"),
    ("Go",         "scaffolder",  "Production-ready web project boilerplate generator"),
]


def get_stars(repo: str) -> int:
    result = subprocess.run(
        ["gh", "api", f"/repos/{OWNER}/{repo}", "--jq", ".stargazers_count"],
        capture_output=True,
        text=True,
        check=True,
    )
    return int(result.stdout.strip())


def build_table() -> str:
    rows = ["| Lang | Project | Description |", "| --- | --- | --- |"]
    for lang, repo, desc in PROJECTS:
        stars = get_stars(repo)
        url = f"https://github.com/{OWNER}/{repo}"
        badge = (
            f" ![Stars](https://img.shields.io/github/stars/{OWNER}/{repo}"
            f"?style=flat-square&color=yellow&label=⭐)"
            if stars > 0
            else ""
        )
        rows.append(f"| `{lang}` | [{repo}]({url}){badge} | {desc} |")
    return "\n".join(rows)


def main():
    readme = "README.md"
    with open(readme) as f:
        content = f.read()

    table = build_table()
    new_content = re.sub(
        r"<!-- PROJECTS-START -->.*?<!-- PROJECTS-END -->",
        f"<!-- PROJECTS-START -->\n{table}\n<!-- PROJECTS-END -->",
        content,
        flags=re.DOTALL,
    )

    with open(readme, "w") as f:
        f.write(new_content)

    print("README updated.")


if __name__ == "__main__":
    main()
