# Build tools

You only need this if you want to **edit lesson content**. The lessons live as plain
markdown in `../course/`. This script turns that markdown into the web deliverables so the
written guide, the pasteable fragments, and the website never drift apart.

## One-time setup

```
pip install -r tools/requirements.txt
```

## Rebuild after editing lessons

From the project root:

```
python tools/build.py
```

That regenerates:

- `web/lesson-*.html` + `web/troubleshooting.html` — pasteable fragments for a custom site
- `docs/index.html` — the full standalone website (served by GitHub Pages)

## Editing tips

- **Lesson text/code:** edit the matching file in `course/` and rerun the build.
- **Brand color / studio name:** change the `TOKENS_LIGHT` / `TOKENS_DARK` values (accent)
  and the bot-name text in `build.py`, then rerun.
- **Add a lesson:** add the markdown file to `course/`, add one row to the `LESSONS` list
  in `build.py`, and rerun.
