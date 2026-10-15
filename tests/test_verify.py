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
