import http.server
import socketserver
import threading
import pytest
from playwright.sync_api import Page
from pathlib import Path
import sys

scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(scripts_dir))
import dev

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

@pytest.fixture(scope="module")
def server():
    handler = dev.PCSSTHandler
    httpd = ReusableTCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()

def test_nav_toggle_escape_key(server, page: Page):
    page.set_viewport_size({"width": 600, "height": 800})
    page.goto(f"{server}/docs/index.html")

    nav_toggle = page.locator("[data-nav-toggle]")
    nav_menu = page.locator("[data-site-menu]")

    nav_toggle.click()
    assert "is-open" in (nav_menu.get_attribute("class") or "")
    assert nav_toggle.get_attribute("aria-expanded") == "true"

    page.keyboard.press("Escape")
    assert "is-open" not in (nav_menu.get_attribute("class") or "")
    assert nav_toggle.get_attribute("aria-expanded") == "false"
    assert page.evaluate("document.activeElement === document.querySelector('[data-nav-toggle]')")

def test_search_input_escape_key(server, page: Page):
    page.goto(f"{server}/docs/search.html")

    search_input = page.locator("[data-doc-search]")
    search_input.fill("theme")
    assert search_input.input_value() == "theme"

    search_input.press("Escape")
    assert search_input.input_value() == ""

    search_input.press("Escape")
    assert page.evaluate("document.activeElement !== document.querySelector('[data-doc-search]')")
