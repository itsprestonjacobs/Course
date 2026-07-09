# Derpy's Designs — Discord Bot Course

A complete, self-teaching course that takes a **total beginner** from installing Python to
running a real Discord bot with branded embeds, moderation commands, and a dropdown ticket
system — no video required. Students read a lesson, type the code, run it, and see it work.

---

## What's in the box

| Folder / file | What it is |
|---------------|-----------|
| **`course/`** | The written guide — 9 markdown lessons + a troubleshooting page. The source of truth for all content. |
| **`bot/`** | The finished **reference bot** students build toward. Fully working; every code snippet in the lessons comes from here. |
| **`docs/`** | The whole course as one **standalone website** — sidebar, one lesson at a time, progress, light/dark toggle. Served by GitHub Pages. |
| **`web/`** | The lessons as **pasteable HTML fragments** — drop them into your own custom website. |
| **`tools/`** | The build script that regenerates `docs/` and `web/` from `course/`. Only needed if you edit lessons. |

---

## How students use it

Pick **one** delivery method — they all teach the same course:

- **Your own website:** paste the files in `web/` into your site's pages. See
  `web/embed-guide.md`.
- **A free hosted site:** GitHub Pages serves the `docs/` folder. See below.
- **Just reading:** open the markdown in `course/` directly.

Whichever they use, they build the bot alongside the lessons and can check their work
against `bot/`.

---

## Publish the site to GitHub Pages

The site lives in `docs/`, which is one of GitHub Pages' built-in source folders.

1. On the repo: **Settings → Pages → Build and deployment → Source:** Deploy from a branch.
2. Choose the `main` branch and the **`/docs`** folder → **Save**.
3. Wait a minute; GitHub shows your live URL, e.g.
   `https://itsprestonjacobs.github.io/Derpybot-/`.

> ⚠️ The `.gitignore` in this project keeps your **bot token** (`.env`) out of GitHub.
> Don't remove that line, and never paste your token into any file you upload.

Full details and rebranding tips are in `docs/README.md`.

---

## Run the reference bot

```
cd bot
pip install -r requirements.txt
copy .env.example .env      # then paste your token into .env
python main.py
```

Getting a token and inviting the bot is taught in **Lesson 03**. The full test checklist is
in `bot/README.md`.

---

## Verification checklist

Run these to confirm the package works end to end:

- [ ] **Bot loads:** `pip install -r bot/requirements.txt`, then `python bot/main.py`
      prints `Logged in as …` and `Synced 8 commands` (needs a real token + test server).
- [ ] **Commands work:** `/serverinfo`, `/announce`, `/kick`, `/timeout`, `/purge`, and
      `/ticketpanel` (dropdown → private channel → Close) all behave. See `bot/README.md`.
- [ ] **Site opens:** double-click `docs/index.html` — sidebar navigation, code copy
      buttons, and the light/dark toggle all work.
- [ ] **Fragments render:** open any file in `web/` in a browser — it displays styled with
      copy buttons.
- [ ] **Rebuild works:** `pip install -r tools/requirements.txt` then `python tools/build.py`
      regenerates `web/` and `docs/` from `course/`.

---

## Rebranding (make it your own)

- **Bot look:** everything branded lives in `bot/config.py` — studio name, tagline, brand
  color, and banner image links. Change it there and the whole bot updates.
- **Course site:** the studio name, logo letter, and accent color are near the top of
  `tools/build.py` (`TOKENS_LIGHT` / `TOKENS_DARK`). Change and rerun the build.

Built for Derpy's Designs • Python + discord.py 2.x.
