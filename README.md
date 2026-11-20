# Pradeep Tarai portfolio

A static one-page portfolio for Pradeep Tarai, graphic designer and video editor. Plain HTML, CSS and JavaScript, no build step needed to host it.

## What is where

| Path | What it is |
| --- | --- |
| `index.html` | The page (generated, see below) |
| `assets/css/` | `tokens.css` (colours, fonts, spacing), `base.css`, `site.css` |
| `assets/js/site.js` | Gallery dialog, reel player, stacking cards, nav highlight |
| `assets/work/` | The 51 posters as WebP (`wNN.webp` full size, `wNN-s.webp` thumbnail) |
| `assets/video/` | The 23 reels, compressed to 720p MP4, with WebP posters |
| `assets/Pradeep-Tarai-CV.pdf` | The CV behind the "Download CV" link |
| `tools/` | `build.py` and `index.template.html`, which generate `index.html` |
| `raw files/`, `reference/` | The originals (379 MB). Git-ignored: they stay on this computer |

## Changing the content

Sector cards, which posters go where, the reels and their captions and the job history all live at the top of `tools/build.py`. Edit the lists, then run:

```bash
python tools/build.py
```

Wording outside those lists (hero, headings, contact) is in `tools/index.template.html`. Needs Python 3 and `ffprobe` (part of FFmpeg) on the PATH.

### Adding a new poster

```bash
ffmpeg -i new.jpg -vf "scale='min(1200,iw)':-2" -c:v libwebp -quality 80 assets/work/w52.webp
```

```bash
ffmpeg -i new.jpg -vf "scale=560:-2" -c:v libwebp -quality 74 assets/work/w52-s.webp
```

Then add `52` to a sector's `all` list in `tools/build.py` and rebuild.

## Preview locally

```bash
python -m http.server 8765
```

Open http://localhost:8765.

## Publish on GitHub Pages

1. Create an empty repository on GitHub (for a root address, name it `<username>.github.io`).
2. From this folder:

```bash
git init -b main
```

```bash
git add . && git commit -m "Portfolio site"
```

```bash
git remote add origin https://github.com/<username>/<repo>.git && git push -u origin main
```

3. On GitHub: Settings, Pages, Source "Deploy from a branch", branch `main`, folder `/ (root)`. The site goes live at `https://<username>.github.io/<repo>/` within a minute or two.

The `.nojekyll` file tells Pages to serve the files as they are. The published site is about 72 MB, well inside the Pages limits.
