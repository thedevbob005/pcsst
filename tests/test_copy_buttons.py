from pathlib import Path
from html.parser import HTMLParser

ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"

class CopyButtonParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.copy_buttons = []

    def handle_starttag(self, tag, attrs):
        if tag == "button":
            attr_dict = dict(attrs)
            if "data-copy" in attr_dict:
                self.copy_buttons.append(attr_dict)

def test_copy_buttons_have_aria_labels():
    for html_file in DOCS_DIR.glob("*.html"):
        parser = CopyButtonParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for button in parser.copy_buttons:
            assert "aria-label" in button, f"Copy button in {html_file.name} missing aria-label"
            assert button["aria-label"] == "Copy code to clipboard", f"Copy button in {html_file.name} has incorrect aria-label: {button['aria-label']}"

def test_app_js_copy_button_aria_handling():
    app_js = (DOCS_DIR / "app.js").read_text(encoding="utf-8")
    assert 'button.setAttribute("aria-label", "Copied to clipboard");' in app_js
    assert 'button.setAttribute("aria-label", "Copy failed");' in app_js
    assert 'button.setAttribute("aria-label", originalAriaLabel);' in app_js
    assert 'button.removeAttribute("aria-label");' in app_js
