from __future__ import annotations

import json
import tarfile
from pathlib import Path

from build import ROOT_DIR
from export_site import export_site
from verify import verify_docs, verify_python


RELEASES_DIR = ROOT_DIR / "releases"
PACKAGE_FILES = ["dist", "src", "docs", "README.md", "LICENSE", "package.json"]


def create_package() -> Path:
    package = json.loads((ROOT_DIR / "package.json").read_text(encoding="utf-8"))
    version = package["version"]
    archive_path = RELEASES_DIR / f"pcsst-{version}.tgz"

    export_site()
    verify_python()
    verify_docs()

    RELEASES_DIR.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive_path, "w:gz") as archive:
        for relative_name in PACKAGE_FILES:
            source = ROOT_DIR / relative_name
            archive.add(source, arcname=f"pcsst-{version}/{relative_name}")

    return archive_path


def main() -> None:
    archive_path = create_package()
    print(f"Created release package at {archive_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
