"""Builds index.html from the asset lists below.

Run from the repo root:  python tools/build.py
Edit SECTORS / REELS / ROLES to change what the page shows, then re-run.
"""
import json
import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "assets" / "work"

EMAIL = "pradeeptarai738@gmail.com"
PHONE_1 = "+91 85954 32752"
PHONE_2 = "+91 95608 48170"
WHATSAPP = "https://wa.me/918595432752"
BEHANCE = "https://www.behance.net/pradeeptarai"

# Each sector is one stacked card. `show` = the three thumbnails on the card,
# `all` = everything in the gallery dialog.
SECTORS = [
    {
        "id": "jewellery", "tone": "wine",
        "title": "Gold that looks worth the trip",
        "line": "Launch posts, festive offers and exhibition invites for jewellers across Odisha.",
        "clients": "Kalamandir, Mahesh, Dharitri, Zever, 22 Carats",
        "show": [3, 6, 46],
        "all": [3, 4, 5, 6, 9, 21, 25, 32, 41, 43, 44, 46, 28, 30, 31, 37, 1],
    },
    {
        "id": "drinks", "tone": "lime",
        "title": "Cans and bottles with a punch",
        "line": "Product ads where the drink is the hero: splash, fruit and a line you remember.",
        "clients": "MBS Lime Up, Hazam Jeera, Gharana Cakes",
        "show": [49, 36, 51],
        "all": [49, 50, 36, 40, 51, 24, 19, 2],
    },
    {
        "id": "travel", "tone": "orange",
        "title": "Trips people want to book",
        "line": "Holiday packages, adventure drops and long-weekend offers built to get the call.",
        "clients": "Amazing Destination, Anokha Safar",
        "show": [12, 16, 7],
        "all": [12, 11, 16, 7, 15],
    },
    {
        "id": "identity", "tone": "cobalt",
        "title": "Logos that hold up small",
        "line": "Marks and wordmarks for agencies, consultants and a civil-engineering school.",
        "clients": "Anokha Safar, Shrijiars, JMD, Rajesh Kukreti, Sanjeev Choudhary",
        "show": [17, 18, 34],
        "all": [17, 18, 33, 34, 13, 14, 10],
    },
    {
        "id": "retail", "tone": "umber",
        "title": "Shops, homes and classrooms",
        "line": "Fashion drops, supermarket offers, venues, eyewear and course admissions.",
        "clients": "Ashoka Fashion Bazar, Bishnupriya, JMD, Optical Express, Gyan Sansar",
        "show": [48, 23, 35],
        "all": [48, 42, 38, 26, 29, 27, 23, 20, 35, 39, 45, 47, 8, 22],
    },
]

# (file number, caption). The first 8 are shown, the rest behind "Show all".
REELS = [
    (6, "Ashoka, Diwali"), (18, "MBS Lime Up"), (22, "Modi travel bags, Diwali"),
    (2, "Kisna jewellery"), (23, "Dharitri Jewellers"), (7, "OGA Home"),
    (1, "MBS drinks"), (17, "Interior walkthrough"),
    (5, "Jewellery campaign"), (20, "Jaihind Jewellers"), (21, "MBS Lime Up"),
    (19, "Modi travel bags"), (3, "Talking-head edit"), (4, "JMD import and export"),
    (8, "Shrijiars"), (9, "Shrijiars Urbania"), (13, "Shrijiars"),
    (10, "Dikhbig"), (11, "Dikhbig, Google Ads"), (12, "Dikhbig, search"),
    (14, "Dikhbig"), (15, "Optical Express"), (16, "Furniture spot"),
]
REELS_SHOWN = 8

ROLES = [
    ("Aug 2026", "Nov 2026", "Think Digital", "Chandrasekharpur, Bhubaneswar", "Graphic designer and video editor"),
    ("Jul 2025", "May 2026", "Dikhbig Performance Marketing Agency", "Bhikaji Cama Place, New Delhi", "Graphic designer"),
    ("Mar 2023", "May 2025", "AMAX Partner in Web Success", "Janakpuri West, New Delhi", "Graphic designer"),
    ("Aug 2022", "Oct 2022", "Agri Link Food Processing", "Bhubaneswar, Odisha", "Graphic designer"),
]


def dims(path: Path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip().split(",")
    return int(out[0]), int(out[1])


def thumb(n, cls="", eager=False):
    w, h = dims(WORK / f"w{n:02d}-s.webp")
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="assets/work/w{n:02d}-s.webp" width="{w}" height="{h}" '
            f'alt="" {load}>')


def card(i, s):
    shots = "\n".join(f'          <li>{thumb(n)}</li>' for n in s["show"])
    return f"""
    <article class="sector sector--{s['tone']}" id="{s['id']}" style="--i:{i}" aria-labelledby="{s['id']}-h">
      <div class="sector__text">
        <h3 id="{s['id']}-h">{escape(s['title'])}</h3>
        <p class="sector__line">{escape(s['line'])}</p>
        <p class="sector__clients">For {escape(s['clients'])}</p>
        <button type="button" class="chip" data-gallery="{s['id']}" hidden>Open all {len(s['all'])} posts</button>
      </div>
      <ul class="sector__shots" role="list" aria-label="{escape(s['title'])}, selected posts">
{shots}
      </ul>
    </article>"""


def reel(idx, n, cap):
    w, h = dims(ROOT / "assets" / "video" / f"reel-{n:02d}.webp")
    more = ' data-more' if idx >= REELS_SHOWN else ''
    return f"""
      <li class="reel"{more}>
        <figure>
          <div class="reel__frame">
            <video preload="none" playsinline controls poster="assets/video/reel-{n:02d}.webp" width="{w}" height="{h}" aria-label="{escape(cap)} reel">
              <source src="assets/video/reel-{n:02d}.mp4" type="video/mp4">
            </video>
          </div>
          <figcaption>{escape(cap)}</figcaption>
        </figure>
      </li>"""


def role(r):
    start, end, co, place, title = r
    return f"""
        <li class="role">
          <p class="role__when num"><time>{start}</time> to <time>{end}</time></p>
          <div>
            <h3 class="role__co">{escape(co)}</h3>
            <p class="role__place">{escape(place)}</p>
          </div>
          <p class="role__title">{escape(title)}</p>
        </li>"""


def main():
    tpl = (ROOT / "tools" / "index.template.html").read_text(encoding="utf-8")
    total = sum(len(s["all"]) for s in SECTORS)
    gallery = {s["id"]: {"title": s["title"], "items": [[n, *dims(WORK / f"w{n:02d}-s.webp")] for n in s["all"]]} for s in SECTORS}
    html = (tpl
            .replace("{{SECTORS}}", "".join(card(i, s) for i, s in enumerate(SECTORS)))
            .replace("{{REELS}}", "".join(reel(i, n, c) for i, (n, c) in enumerate(REELS)))
            .replace("{{REEL_COUNT}}", str(len(REELS)))
            .replace("{{POST_COUNT}}", str(total))
            .replace("{{ROLES}}", "".join(role(r) for r in ROLES))
            .replace("{{GALLERY_JSON}}", json.dumps(gallery))
            .replace("{{EMAIL}}", EMAIL)
            .replace("{{PHONE_1}}", PHONE_1)
            .replace("{{PHONE_1_TEL}}", PHONE_1.replace(" ", ""))
            .replace("{{PHONE_2}}", PHONE_2)
            .replace("{{PHONE_2_TEL}}", PHONE_2.replace(" ", ""))
            .replace("{{WHATSAPP}}", WHATSAPP)
            .replace("{{BEHANCE}}", BEHANCE)
            .replace("{{HERO_A}}", thumb(50, "hero__poster hero__poster--a", eager=True))
            .replace("{{HERO_B}}", thumb(5, "hero__poster hero__poster--b", eager=True)))
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"index.html written: {len(SECTORS)} sectors, {total} posts, {len(REELS)} reels")


if __name__ == "__main__":
    main()
