
import os
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List, Tuple
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv

API = "https://api.github.com"


def auth_headers(token: str | None) -> Dict[str, str]:
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "github-portfolio-generator",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def gh_get(url: str, headers: Dict[str, str], params: Dict[str, str] | None = None) -> requests.Response:
    """GET with basic retry on 403 rate limit and 5xx."""
    retries = 3
    backoff = 2
    for _ in range(retries):
        r = requests.get(url, headers=headers, params=params, timeout=30)
        if r.status_code == 403 and "rate limit" in r.text.lower():
            time.sleep(backoff)
            backoff *= 2
            continue
        if r.status_code >= 500:
            time.sleep(backoff)
            backoff *= 2
            continue
        return r
    return r


def get_user(username: str, headers: Dict[str, str]) -> Dict:
    r = gh_get(f"{API}/users/{username}", headers=headers)
    r.raise_for_status()
    return r.json()


def iter_repos(username: str, headers: Dict[str, str]):
    """Yield all repos (public) with pagination."""
    page = 1
    per_page = 100
    while True:
        r = gh_get(f"{API}/users/{username}/repos", headers=headers, params={"per_page": per_page, "page": page, "sort": "updated"})
        r.raise_for_status()
        items = r.json()
        if not items:
            break
        for it in items:
            yield it
        page += 1


def compute_top_languages(repos: List[Dict]) -> List[Tuple[str, float]]:
    """Compute top languages by counting repo.language (cheap heuristic)."""
    counts: Dict[str, int] = {}
    total = 0
    for r in repos:
        lang = r.get("language")
        if not lang:
            continue
        counts[lang] = counts.get(lang, 0) + 1
        total += 1
    if total == 0:
        return []
    items = [(lang, (count / total) * 100.0) for lang, count in counts.items()]
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:6]


def humanize_datetime(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z","+00:00"))
    except Exception:
        return iso
    delta = datetime.now(timezone.utc) - dt
    secs = int(delta.total_seconds())
    if secs < 60: return f"hace {secs}s"
    mins = secs // 60
    if mins < 60: return f"hace {mins}min"
    hrs = mins // 60
    if hrs < 24: return f"hace {hrs}h"
    days = hrs // 24
    if days < 30: return f"hace {days}d"
    months = days // 30
    if months < 12: return f"hace {months} meses"
    years = months // 12
    return f"hace {years} años"


def select_top_repos(repos: List[Dict], n:int=6) -> List[Dict]:
    items = [r for r in repos if not r.get("fork") and not r.get("archived")]
    items.sort(key=lambda r: (r.get("stargazers_count",0), r.get("forks_count",0)), reverse=True)
    return items[:n]


def select_recent_repos(repos: List[Dict], n:int=6) -> List[Dict]:
    items = [r for r in repos if not r.get("fork")]
    items.sort(key=lambda r: r.get("pushed_at",""), reverse=True)
    for it in items:
        it["pushed_at_human"] = humanize_datetime(it.get("pushed_at",""))
    return items[:n]


def render_readme(context: Dict, output_path: Path) -> bool:
    here = Path(__file__).resolve().parent
    env = Environment(
        loader=FileSystemLoader(str(here)),
        autoescape=select_autoescape(enabled_extensions=("html","md","md.j2","j2")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("template.md.j2")
    html = template.render(**context)
    output_path.write_text(html, encoding="utf-8")
    return True


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    load_dotenv()
    username = None
    for i, a in enumerate(argv):
        if a in ("-u","--username") and i+1 < len(argv):
            username = argv[i+1]
    if not username:
        username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")

    if not username:
        print("ERROR: falta GITHUB_USERNAME o --username", file=sys.stderr)
        return 2

    headers = auth_headers(token)
    user = get_user(username, headers)
    repos = list(iter_repos(username, headers))

    top_languages = compute_top_languages(repos)
    top_repos = select_top_repos(repos, n=6)
    recent_repos = select_recent_repos(repos, n=6)

    ctx = {
        "user": user,
        "tagline": "Full‑stack developer · Automatización · APIs",
        "top_languages": top_languages,
        "top_repos": top_repos,
        "recent_repos": recent_repos,
        "now_iso": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    out = Path(__file__).resolve().parent / "README.md"
    render_readme(ctx, out)
    print(f"README generado en {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
