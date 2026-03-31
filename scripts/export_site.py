from __future__ import annotations

import shutil
from pathlib import Path

from build import ROOT_DIR, build


SITE_DIR = ROOT_DIR / "site"
SITE_FILES = ["index.html", "docs", "dist"]


def export_site() -> Path:
    build()

    if SITE_DIR.exists():
        try:
            shutil.rmtree(SITE_DIR)
        except FileNotFoundError:
            pass

    SITE_DIR.mkdir(parents=True, exist_ok=True)

    for relative_name in SITE_FILES:
        source = ROOT_DIR / relative_name
        destination = SITE_DIR / relative_name
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copyfile(source, destination)

    (SITE_DIR / "404.html").write_text(
        """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url=docs/index.html" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>PCSST</title>
  </head>
  <body>
    <p>
      Redirecting to the PCSST docs.
      <a href="docs/index.html">Open the site</a>.
    </p>
  </body>
</html>
""",
        encoding="utf-8",
    )
    return SITE_DIR


def main() -> None:
    site_dir = export_site()
    print(f"Exported site to {site_dir.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
