from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


# Add scripts directory to sys.path to import the build module
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(SCRIPTS_DIR))

import build


def test_minify_css() -> None:
    source = "  body {  color: red;  }  /* comment */  .class { margin: 10px 20px; } "
    expected = "body{color:red}.class{margin:10px 20px}"
    assert build.minify_css(source) == expected


def test_build(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Setup temporary directory structure
    root_dir = tmp_path
    src_dir = root_dir / "src"
    src_dir.mkdir()
    docs_dir = root_dir / "docs"
    docs_dir.mkdir()

    package_json = root_dir / "package.json"
    package_json.write_text(json.dumps({"version": "1.2.3"}), encoding="utf-8")

    source_css = src_dir / "pcsst.css"
    source_css.write_text("body { color: blue; }\n/* Test comment */\n.btn { padding: 5px; }", encoding="utf-8")

    # Monkeypatch constants in the build module to use our temporary directory
    monkeypatch.setattr(build, "ROOT_DIR", root_dir)
    monkeypatch.setattr(build, "SOURCE_PATH", source_css)
    monkeypatch.setattr(build, "DIST_DIR", root_dir / "dist")
    monkeypatch.setattr(build, "DIST_PATH", root_dir / "dist" / "pcsst.css")
    monkeypatch.setattr(build, "DIST_MIN_PATH", root_dir / "dist" / "pcsst.min.css")
    monkeypatch.setattr(build, "DOCS_DIST_DIR", root_dir / "docs" / "dist")
    monkeypatch.setattr(build, "DOCS_DIST_PATH", root_dir / "docs" / "dist" / "pcsst.css")
    monkeypatch.setattr(build, "DOCS_DIST_MIN_PATH", root_dir / "docs" / "dist" / "pcsst.min.css")

    # Run the build function
    dist_path, dist_min_path = build.build()

    # Verifications
    banner = "/*! PCSST v1.2.3 | MIT License */\n"
    expected_source = "body { color: blue; }\n/* Test comment */\n.btn { padding: 5px; }"
    expected_minified = "body{color:blue}.btn{padding:5px}"

    # Check dist files
    assert dist_path.exists()
    assert dist_path.read_text(encoding="utf-8") == f"{banner}{expected_source}\n"

    assert dist_min_path.exists()
    assert dist_min_path.read_text(encoding="utf-8") == f"{banner}{expected_minified}\n"

    # Check docs/dist files
    docs_dist_path = root_dir / "docs" / "dist" / "pcsst.css"
    docs_dist_min_path = root_dir / "docs" / "dist" / "pcsst.min.css"

    assert docs_dist_path.exists()
    assert docs_dist_path.read_text(encoding="utf-8") == dist_path.read_text(encoding="utf-8")

    assert docs_dist_min_path.exists()
    assert docs_dist_min_path.read_text(encoding="utf-8") == dist_min_path.read_text(encoding="utf-8")

    # Check return values
    assert dist_path == root_dir / "dist" / "pcsst.css"
    assert dist_min_path == root_dir / "dist" / "pcsst.min.css"
