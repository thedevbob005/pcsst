# PCSST

PCSST stands for Perfect CSS Treasure.

It is a pure CSS framework that combines:

- design tokens through CSS custom properties
- readable layout and spacing utilities
- responsive utility tiers
- ready-to-use interface components
- theme support without a build step
- a documentation site with its own visual identity
- release automation for verification, packaging, and docs deployment

## Links

- Repository: `https://github.com/thedevbob005/pcsst`
- Docs: `https://thedevbob005.github.io/pcsst/`

## Project Structure

- `src/pcsst.css`: authoring source for the framework
- `dist/pcsst.css`: distributable framework build
- `dist/pcsst.min.css`: minified build
- `docs/`: documentation site and showcase
- `.github/workflows/`: CI, Pages deployment, and release automation
- `.editorconfig` and `.gitattributes`: repository defaults for text and formatting
- `scripts/build.py`: build script
- `scripts/verify.py`: verification for scripts and docs references
- `scripts/export_site.py`: static export for deployment
- `scripts/package.py`: release archive creation
- `scripts/dev.py`: zero-dependency static server

## Quick Start

```html
<link rel="stylesheet" href="dist/pcsst.css" />

<section class="shell section stack stack-4">
  <span class="badge badge--accent">PCSST</span>
  <h1 class="display">Human-readable CSS for teams.</h1>
  <p class="lead">Build layouts, components, and themes with plain CSS.</p>
  <div class="cluster md-cluster-wide">
    <a class="button button--primary" href="#">Launch</a>
    <a class="button button--ghost" href="#">Read docs</a>
  </div>
</section>
```

## Commands

```bash
python3 scripts/build.py
python3 scripts/verify.py
python3 scripts/dev.py
python3 scripts/export_site.py
python3 scripts/package.py
```

The docs server runs at `http://localhost:4173`.

## Docs Map

- `docs/index.html`: project overview
- `docs/getting-started.html`: installation and workflow guide
- `docs/library.html`: token, utility, and component reference
- `docs/themes.html`: theming guide
- `docs/showcase.html`: composed UI examples
- `docs/search.html`: static docs search
- `docs/changelog.html`: release notes and roadmap
