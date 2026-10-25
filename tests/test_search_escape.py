import http.server
import socketserver
import threading
import time
from pathlib import Path
import pytest
from playwright.sync_api import Page

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

@pytest.fixture(scope="module")
def server():
    repo_root = Path(__file__).resolve().parent.parent
    handler = http.server.SimpleHTTPRequestHandler

    class DirectoryHandler(handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(repo_root), **kwargs)

    httpd = ReusableTCPServer(("127.0.0.1", 4174), DirectoryHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.2)
    yield "http://127.0.0.1:4174"
    httpd.shutdown()
    httpd.server_close()

def test_search_escape_clears_text_and_blurs(page: Page, server: str):
    page.goto(f"{server}/docs/search.html")

    search_input = page.locator("[data-doc-search]")
    search_input.wait_for()

    # Fill search input
    search_input.fill("theme")
    assert page.locator("[data-search-results] article").count() > 0

    # Press Escape when text is present -> clears input
    search_input.press("Escape")
    assert search_input.input_value() == ""

    # Press Escape again when empty -> blurs input
    search_input.press("Escape")
    is_focused = page.evaluate("document.activeElement === document.querySelector('[data-doc-search]')")
    assert not is_focused
