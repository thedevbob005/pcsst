import threading
import http.server
import socketserver
import pytest
from playwright.sync_api import sync_playwright, expect
from pathlib import Path

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

@pytest.fixture(scope="module")
def server():
    handler = http.server.SimpleHTTPRequestHandler
    httpd = ReusableTCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    yield f"http://127.0.0.1:{port}"

    httpd.shutdown()

def test_command_card_copy_button(server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.add_init_script("""
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: async (text) => { window.__copiedText = text; }
                },
                configurable: true
            });
        """)

        page.goto(f"{server}/docs/index.html")

        copy_button = page.locator(".command-card button[data-copy]").first
        expect(copy_button).to_be_visible()
        expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")

        copy_button.click()

        expect(copy_button).to_have_text("Copied")
        expect(copy_button).to_have_class("button button--ghost button--sm is-valid")
        expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")

        copied = page.evaluate("window.__copiedText")
        assert "python3 scripts/build.py" in copied

        browser.close()
