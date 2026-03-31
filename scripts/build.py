from __future__ import annotations

import json
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_PATH = ROOT_DIR / "src" / "pcsst.css"
DIST_DIR = ROOT_DIR / "dist"
DIST_PATH = DIST_DIR / "pcsst.css"
DIST_MIN_PATH = DIST_DIR / "pcsst.min.css"


def minify_css(source: str) -> str:
    without_comments = re.sub(r"/\*[\s\S]*?\*/", "", source)
    collapsed = re.sub(r"\s+", " ", without_comments)
    tightened = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", collapsed)
    return tightened.replace(";}", "}").strip()


def build() -> tuple[Path, Path]:
    package = json.loads((ROOT_DIR / "package.json").read_text(encoding="utf-8"))
    source = SOURCE_PATH.read_text(encoding="utf-8").strip()
    banner = f"/*! PCSST v{package['version']} | MIT License */\n"

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DIST_PATH.write_text(f"{banner}{source}\n", encoding="utf-8")
    DIST_MIN_PATH.write_text(f"{banner}{minify_css(source)}\n", encoding="utf-8")

    return DIST_PATH, DIST_MIN_PATH


def main() -> None:
    dist_path, dist_min_path = build()

    print(f"Built {dist_path.relative_to(ROOT_DIR)}")
    print(f"Built {dist_min_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
