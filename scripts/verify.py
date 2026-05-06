from __future__ import annotations

import sys
import subprocess
from html.parser import HTMLParser
from pathlib import Path

from build import ROOT_DIR, build


DOCS_DIR = ROOT_DIR / "docs"
SCRIPT_FILES = [
    ROOT_DIR / "scripts" / "build.py",
    ROOT_DIR / "scripts" / "dev.py",
    ROOT_DIR / "scripts" / "export_site.py",
    ROOT_DIR / "scripts" / "package.py",
    ROOT_DIR / "scripts" / "verify.py",
    ROOT_DIR / "tests" / "test_build.py",
    ROOT_DIR / "tests" / "test_package.py",
    ROOT_DIR / "tests" / "test_verify.py",
]


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in ("link", "script", "a"):
            return

        attr_map = dict(attrs)

        if tag == "link":
            if attr_map.get("rel") != "icon":
                href = attr_map.get("href")
                if href:
                    self.references.append(href)

        elif tag == "script":
            src = attr_map.get("src")
            if src:
                self.references.append(src)

        elif tag == "a":
            href = attr_map.get("href")
            if href and href.startswith("./"):
                self.references.append(href)


def verify_python() -> None:
    for script_file in SCRIPT_FILES:
        source = script_file.read_text(encoding="utf-8")
        compile(source, str(script_file), "exec")


def verify_tests() -> None:
    subprocess.check_call([sys.executable, "-m", "pytest"])


def verify_docs() -> None:
    issues: list[str] = []
    checked_refs: dict[tuple[Path, str], bool] = {}

    for html_file in DOCS_DIR.glob("*.html"):
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for ref in parser.references:
            if ref.startswith("http"):
                continue

            ref_path = ref.split("#", 1)[0]
            if not ref_path:
                continue

            cache_key = (html_file.parent, ref_path)
            if cache_key not in checked_refs:
                target = (html_file.parent / ref_path).resolve()
                checked_refs[cache_key] = target.exists()

            if not checked_refs[cache_key]:
                issues.append(f"{html_file.name}: missing {ref_path}")

    if issues:
        raise SystemExit("\n".join(issues))


def main() -> None:
    build()
    verify_python()
    verify_tests()
    verify_docs()

    print("Built framework assets")
    print("Verified Python scripts")
    print("Verified Python tests")
    print("Verified documentation references")


if __name__ == "__main__":
    main()
