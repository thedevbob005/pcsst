import sys
from pathlib import Path

# Add scripts directory to sys.path
scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(scripts_dir))

from verify import ReferenceParser

def test_reference_parser_link():
    parser = ReferenceParser()
    html = '<link rel="stylesheet" href="style.css"><link rel="icon" href="favicon.ico">'
    parser.feed(html)
    assert "style.css" in parser.references
    assert "favicon.ico" not in parser.references

def test_reference_parser_script():
    parser = ReferenceParser()
    html = '<script src="app.js"></script><script>console.log("hello")</script>'
    parser.feed(html)
    assert "app.js" in parser.references
    assert len(parser.references) == 1

def test_reference_parser_a_tag():
    parser = ReferenceParser()
    html = '<a href="./page.html">Local</a><a href="https://example.com">External</a><a href="page2.html">Relative but no ./</a>'
    parser.feed(html)
    assert "./page.html" in parser.references
    assert "https://example.com" not in parser.references
    assert "page2.html" not in parser.references

def test_reference_parser_mixed():
    parser = ReferenceParser()
    html = """
    <html>
        <head>
            <link rel="stylesheet" href="./css/main.css">
            <script src="./js/main.js"></script>
        </head>
        <body>
            <a href="./about.html">About</a>
            <a href="http://google.com">Google</a>
        </body>
    </html>
    """
    parser.feed(html)
    assert "./css/main.css" in parser.references
    assert "./js/main.js" in parser.references
    assert "./about.html" in parser.references
    assert "http://google.com" not in parser.references
    assert len(parser.references) == 3

def test_copy_buttons_aria_labels():
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    html_files = list(docs_dir.glob("*.html"))
    assert len(html_files) > 0, "No HTML files found in docs/"

    copy_buttons_found = 0
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        if "data-copy" in content:
            # Check every data-copy button in this file
            for line in content.splitlines():
                if "data-copy" in line:
                    copy_buttons_found += 1
                    assert 'aria-label="' in line, f"data-copy button missing aria-label in {html_file.name}: {line.strip()}"

    assert copy_buttons_found > 0, "No data-copy buttons found across docs HTML files"
