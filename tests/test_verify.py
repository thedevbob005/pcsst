import sys
from pathlib import Path
import pytest

# Add scripts directory to sys.path
scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(scripts_dir))

from verify import ReferenceParser, verify_docs

def test_reference_parser_link():
    parser = ReferenceParser()
    parser.feed('<link rel="stylesheet" href="./style.css">')
    parser.feed('<link rel="icon" href="./favicon.ico">')
    parser.feed('<link rel="stylesheet" href="https://example.com/style.css">')
    assert "./style.css" in parser.references
    assert "./favicon.ico" not in parser.references
    assert "https://example.com/style.css" in parser.references

def test_reference_parser_script():
    parser = ReferenceParser()
    parser.feed('<script src="./app.js"></script>')
    parser.feed('<script src="https://example.com/app.js"></script>')
    assert "./app.js" in parser.references
    assert "https://example.com/app.js" in parser.references

def test_reference_parser_a():
    parser = ReferenceParser()
    parser.feed('<a href="./library.html">Library</a>')
    # a tags MUST start with ./ according to verify.py logic
    parser.feed('<a href="https://example.com">External</a>')
    parser.feed('<a href="other.html">Not relative</a>')
    parser.feed('<a href="#fragment">Fragment</a>')
    assert parser.references == ["./library.html"]

def test_verify_docs_success(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    html_file = docs_dir / "index.html"
    html_file.write_text(
        '<html>'
        '<link rel="stylesheet" href="./style.css">'
        '<link rel="stylesheet" href="https://example.com/external.css">'
        '<script src="./app.js"></script>'
        '<script src="https://example.com/external.js"></script>'
        '<a href="./other.html">Link</a>'
        '<a href="./other.html#section">Link with fragment</a>'
        '</html>',
        encoding="utf-8"
    )

    (docs_dir / "style.css").write_text("", encoding="utf-8")
    (docs_dir / "app.js").write_text("", encoding="utf-8")
    (docs_dir / "other.html").write_text("", encoding="utf-8")

    # We monkeypatch the DOCS_DIR in the verify module
    import verify
    monkeypatch.setattr(verify, "DOCS_DIR", docs_dir)

    # Should not raise SystemExit
    verify_docs()

def test_verify_docs_failure(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    html_file = docs_dir / "index.html"
    html_file.write_text(
        '<html><link rel="stylesheet" href="./missing.css"></html>',
        encoding="utf-8"
    )

    import verify
    monkeypatch.setattr(verify, "DOCS_DIR", docs_dir)

    with pytest.raises(SystemExit) as excinfo:
        verify_docs()

    assert "index.html: missing ./missing.css" in str(excinfo.value)
