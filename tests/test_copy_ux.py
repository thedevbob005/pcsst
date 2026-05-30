import pytest
import subprocess
import time
import socket
from playwright.sync_api import sync_playwright

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

@pytest.fixture(scope="module")
def dev_server():
    port = 4173
    # Start the dev server
    process = subprocess.Popen(["python3", "scripts/dev.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to be ready
    start_time = time.time()
    while time.time() - start_time < 5:
        if is_port_open(port):
            break
        time.sleep(0.5)
    else:
        process.kill()
        pytest.fail("Dev server failed to start")

    yield f"http://127.0.0.1:{port}"

    process.kill()

def test_copy_button_ux(dev_server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Grant clipboard permissions
        context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
        page = context.new_page()

        # Navigate to library.html (via the /docs/ prefix as per dev.py behavior)
        page.goto(f"{dev_server}/docs/library.html")

        # Find the first copy button
        copy_button = page.locator("[data-copy]").first

        # 1. Check initial ARIA label
        assert copy_button.get_attribute("aria-label") == "Copy code to clipboard"

        # 2. Click and check feedback state
        copy_button.click()
        assert copy_button.inner_text() == "Copied"
        assert copy_button.get_attribute("aria-label") == "Copied to clipboard"

        # 3. Test race condition (rapid clicks)
        # We wait a bit then click again
        time.sleep(0.5)
        copy_button.click()
        assert copy_button.inner_text() == "Copied"

        # 4. Wait for restoration
        # Timeout is 1400ms in app.js
        time.sleep(1.5)
        assert copy_button.inner_text() == "Copy"
        assert copy_button.get_attribute("aria-label") == "Copy code to clipboard"

        browser.close()
