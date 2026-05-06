from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_PATH = ROOT_DIR / "src" / "pcsst.css"
DIST_DIR = ROOT_DIR / "dist"
DIST_PATH = DIST_DIR / "pcsst.css"
DIST_MIN_PATH = DIST_DIR / "pcsst.min.css"
DOCS_DIST_DIR = ROOT_DIR / "docs" / "dist"
DOCS_DIST_PATH = DOCS_DIST_DIR / "pcsst.css"
DOCS_DIST_MIN_PATH = DOCS_DIST_DIR / "pcsst.min.css"


def minify_css(source: str) -> str:
    # Remove comments
    without_comments = re.sub(r"/\*[\s\S]*?\*/", "", source)
    # Collapse whitespace
    collapsed = re.sub(r"\s+", " ", without_comments)
    # Remove space around punctuation
    tightened = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", collapsed)
    return tightened.replace(";}", "}").strip()


def resolve_imports(filepath: Path, imported_files: set[Path] | None = None) -> str:
    if imported_files is None:
        imported_files = set()

    if filepath in imported_files:
        return ""

    imported_files.add(filepath)
    content = filepath.read_text(encoding="utf-8")

    def replace_import(match: re.Match) -> str:
        import_path = match.group(1) or match.group(2)
        # Handle layer(...) if present
        full_match = match.group(0)

        target_path = (filepath.parent / import_path).resolve()
        if target_path.exists():
            inner_content = resolve_imports(target_path, imported_files)

            # If it's an @import ... layer(name), wrap content in @layer name { ... }
            layer_match = re.search(r"layer\((.*?)\)", full_match)
            if layer_match:
                layer_name = layer_match.group(1)
                return f"@layer {layer_name} {{\n{inner_content}\n}}\n"
            return inner_content
        return full_match

    # Match @import "path"; or @import 'path'; optionally with layer(...)
    # This is a simple regex, might need refinement for complex imports
    pattern = re.compile(r"@import\s+(?:\"(.*?)\"|'(.*?)')(.*?;)")
    return pattern.sub(replace_import, content)


def build() -> tuple[Path, Path]:
    package = json.loads((ROOT_DIR / "package.json").read_text(encoding="utf-8"))

    # Resolve imports to get the full bundled source
    source = resolve_imports(SOURCE_PATH).strip()

    banner = f"/*! PCSST v{package['version']} | MIT License */\n"

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIST_DIR.mkdir(parents=True, exist_ok=True)

    DIST_PATH.write_text(f"{banner}{source}\n", encoding="utf-8")
    DIST_MIN_PATH.write_text(f"{banner}{minify_css(source)}\n", encoding="utf-8")

    shutil.copyfile(DIST_PATH, DOCS_DIST_PATH)
    shutil.copyfile(DIST_MIN_PATH, DOCS_DIST_MIN_PATH)

    return DIST_PATH, DIST_MIN_PATH


def main() -> None:
    dist_path, dist_min_path = build()

    print(f"Built {dist_path.relative_to(ROOT_DIR)}")
    print(f"Built {dist_min_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
