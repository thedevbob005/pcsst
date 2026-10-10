import sys
import socketserver
import threading
from http.server import SimpleHTTPRequestHandler
import pytest
from playwright.sync_api import Page, expect

from scripts.build import ROOT_DIR


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


@pytest.fixture(scope="module", autouse=True)
def http_server():
    class DocsHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    server = ReusableTCPServer(("127.0.0.1", 0), DocsHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


def test_search_escape_key_clears_query_and_blurs(page: Page, http_server: str):
    page.goto(f"{http_server}/docs/search.html")

    search_input = page.locator("[data-doc-search]")
    expect(search_input).to_be_visible()

    # Fill search input
    search_input.fill("responsive")
    expect(search_input).to_have_value("responsive")

    # Press Escape to clear
    search_input.press("Escape")
    expect(search_input).to_have_value("")

    # Verify results reset to default count / state
    search_count = page.locator("[data-search-count]")
    expect(search_count).to_contain_text("docs entries")

    # Press Escape on empty input to blur
    search_input.press("Escape")
    is_focused = page.evaluate("document.activeElement === document.querySelector('[data-doc-search]')")
    assert not is_focused
