import http.server
import socketserver
import threading
import pytest
from playwright.sync_api import sync_playwright

class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

@pytest.fixture(scope="module")
def server():
    handler = http.server.SimpleHTTPRequestHandler
    httpd = ReuseAddrTCPServer(("127.0.0.1", 4173), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    yield httpd
    httpd.shutdown()
    httpd.server_close()

def test_nav_toggle_escape(server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 600, "height": 800})
        page.goto("http://127.0.0.1:4173/docs/index.html")

        toggle = page.locator("[data-nav-toggle]")
        menu = page.locator("[data-site-menu]")

        toggle.click()
        assert menu.evaluate("el => el.classList.contains('is-open')") is True
        assert toggle.get_attribute("aria-expanded") == "true"

        page.keyboard.press("Escape")

        assert menu.evaluate("el => el.classList.contains('is-open')") is False
        assert toggle.get_attribute("aria-expanded") == "false"
        assert page.evaluate("document.activeElement === document.querySelector('[data-nav-toggle]')") is True

        browser.close()

def test_search_escape(server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:4173/docs/search.html")

        search_input = page.locator("[data-doc-search]")
        search_input.fill("responsive")
        assert search_input.input_value() == "responsive"

        search_input.press("Escape")
        assert search_input.input_value() == ""

        # Pressing escape on empty input blurs the input
        search_input.press("Escape")
        assert page.evaluate("document.activeElement === document.querySelector('[data-doc-search]')") is False

        browser.close()
