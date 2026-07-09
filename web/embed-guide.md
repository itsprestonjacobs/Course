# Using the web lesson fragments

This folder has one **self-contained HTML file per lesson** (`lesson-00.html` …
`lesson-08.html`, plus `troubleshooting.html`). Each file already includes its own styles
and a copy-to-clipboard button on every code block, so you can drop it straight into your
custom website with no extra setup.

## How to use them

**If your site has a "custom HTML" or "embed" block** (most site builders and CMSes do):
1. Open the lesson file (e.g. `lesson-05.html`) in a text editor.
2. Copy everything.
3. Paste it into the HTML/embed block for that lesson's page.

That's it — the lesson renders with headings, formatted code, callouts, and copy buttons.

**If your site renders raw HTML from files**, just serve these files directly.

## Good to know

- **Scoped styles.** Everything is wrapped in `<section class="ddc">` and every style rule
  is prefixed with `.ddc`, so the fragment won't fight your site's existing CSS.
- **Light & dark.** The fragments follow the visitor's system theme automatically.
- **Brand color.** The accent is Derpy blue (`#1e9bff`). To rebrand, find `--ddc-accent`
  near the top of the `<style>` block in each file and change the hex value.
- **No internet needed.** No external fonts, scripts, or images — everything is inline, so
  the fragments work offline and never break from a broken link.

## Prefer a whole ready-made website?

If you'd rather host the entire course as its own site (recommended for GitHub Pages), use
the `docs/` folder instead — it's a complete website with a sidebar, navigation, progress
tracking, and a theme toggle. See `docs/README.md` for one-click GitHub Pages steps.

## Want to regenerate these?

The fragments are generated from the markdown in `course/`. If you edit a lesson there, the
studio can re-run the build script to refresh both these fragments and the full site, so
the code, the written guide, and the website never drift apart.
