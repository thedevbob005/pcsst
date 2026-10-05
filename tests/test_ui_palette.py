import http.server
import socketserver
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def run_server(port, ready_event, stop_event):
    handler = http.server.SimpleHTTPRequestHandler
    class QuietHandler(handler):
        def log_message(self, format, *args):
            pass

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    with ReusableTCPServer(("127.0.0.1", port), QuietHandler) as httpd:
        httpd.timeout = 0.5
        ready_event.set()
        while not stop_event.is_set():
            httpd.handle_request()

def test_copy_button_interaction():
    port = 8912
    ready_event = threading.Event()
    stop_event = threading.Event()
    server_thread = threading.Thread(target=run_server, args=(port, ready_event, stop_event), daemon=True)
    server_thread.start()
    ready_event.wait()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Mock navigator.clipboard
            page.add_init_script("""
                if (!navigator.clipboard) {
                    navigator.clipboard = {};
                }
                navigator.clipboard.writeText = async (text) => {
                    window.__lastCopiedText = text;
                    return Promise.resolve();
                };
            """)

            page.goto(f"http://127.0.0.1:{port}/getting-started.html")

            button = page.locator("button[data-copy]").first
            assert button.inner_text() == "Copy"

            button.click()

            page.wait_for_selector("button[data-copy].is-valid")
            assert button.inner_text() == "Copied"
            assert button.get_attribute("aria-label") == "Copied to clipboard"

            # Check copied content
            copied = page.evaluate("window.__lastCopiedText")
            assert copied is not None and len(copied) > 0

            browser.close()
    finally:
        stop_event.set()
