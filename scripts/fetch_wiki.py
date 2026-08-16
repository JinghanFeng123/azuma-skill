#!/usr/bin/env python3
"""Fetch the latest Azuma (吾妻) page source from the 碧蓝海事局 WIKI.

Use this script when the user asks to refresh the skill's data or when the
references may be outdated. The wiki is a MediaWiki site, so the script uses
the MediaWiki parse API and saves the raw wikitext for manual comparison.

Usage:
    python fetch_wiki.py                    # print a short summary
    python fetch_wiki.py --save path.txt    # save raw wikitext to a file
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

API_URL = "https://wiki.biligame.com/blhx/api.php"
PAGE = "吾妻"
USER_AGENT = "Codex-AzumaSkill/1.0"


def fetch_wikitext(page=PAGE):
    params = urllib.parse.urlencode(
        {
            "action": "parse",
            "page": page,
            "prop": "wikitext",
            "format": "json",
            "formatversion": "2",
        }
    )
    request = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if "parse" not in payload or "wikitext" not in payload["parse"]:
        raise RuntimeError(f"Unexpected API response: {json.dumps(payload, ensure_ascii=False)[:500]}")
    return payload["parse"]["title"], payload["parse"]["wikitext"]


def main():
    parser = argparse.ArgumentParser(description="Fetch Azuma wiki source from 碧蓝海事局 WIKI.")
    parser.add_argument("--save", metavar="PATH", help="Save the raw wikitext to this file.")
    parser.add_argument("--page", default=PAGE, help="Wiki page title (default: 吾妻).")
    args = parser.parse_args()

    try:
        title, wikitext = fetch_wikitext(args.page)
    except Exception as exc:  # noqa: BLE001 - surface any network/parse error to the user
        print(f"[ERROR] Fetch failed: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Fetched '{title}' ({len(wikitext)} chars) from {API_URL}")
    if args.save:
        with open(args.save, "w", encoding="utf-8") as handle:
            handle.write(wikitext)
        print(f"[OK] Saved wikitext to {args.save}")
    else:
        print(wikitext[:300].replace("\n", " "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
