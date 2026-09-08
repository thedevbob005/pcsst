import http.server
import socketserver
import threading
import time
import pytest

PORT = 4173

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

Handler = http.server.SimpleHTTPRequestHandler

@pytest.fixture(scope="module", autouse=True)
def server():
    httpd = ReusableTCPServer(("", PORT), Handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    time.sleep(0.5)
    yield httpd
    httpd.shutdown()
    httpd.server_close()

def test_copy_button_feedback(page):
    # Mock clipboard
    page.add_init_script("""
        if (!navigator.clipboard) {
            navigator.clipboard = {};
        }
        navigator.clipboard.writeText = async () => {};
    """)

    page.goto(f"http://127.0.0.1:{PORT}/docs/library.html")

    # Find first copy button in library.html
    copy_btn = page.locator(".code-card button[data-copy]").first
    assert copy_btn.is_visible()

    # Click copy button
    copy_btn.click()

    # Check feedback state: text updated, class .is-valid added, aria-label set
    assert copy_btn.text_content().strip() == "Copied"
    assert "is-valid" in (copy_btn.get_attribute("class") or "").split()
    assert copy_btn.get_attribute("aria-label") == "Copied to clipboard"

    # Wait for timeout reset (1400ms)
    page.wait_for_timeout(1600)

    # Check restored state
    assert copy_btn.text_content().strip() == "Copy"
    assert "is-valid" not in (copy_btn.get_attribute("class") or "").split()
