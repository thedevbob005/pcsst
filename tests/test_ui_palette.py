import re
import socket
import subprocess
import time
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="session", autouse=True)
def dev_server():
    # Start dev server
    process = subprocess.Popen(["python3", "scripts/dev.py"])
    # Wait for port 4173 to open
    start_time = time.time()
    while time.time() - start_time < 5:
        try:
            with socket.create_connection(("127.0.0.1", 4173), timeout=1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        process.terminate()
        raise RuntimeError("Development server did not start on port 4173")

    yield

    process.terminate()
    process.wait()

def test_search_shortcut_indicator(page: Page):
    # Navigate explicitly to the HTML file path
    page.goto("http://127.0.0.1:4173/docs/search.html")

    # Check that the shortcut element is visible
    shortcut = page.locator("[data-search-shortcut]")
    assert shortcut.is_visible()

    # In Linux test environment, it should be Ctrl+K
    assert shortcut.text_content() == "Ctrl+K"

def test_keyboard_shortcut_focuses_input(page: Page):
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Press Control+K
    page.keyboard.press("Control+k")

    # Expect redirect or focus on search.html
    page.wait_for_url("**/search.html")

    is_focused = page.evaluate("document.activeElement === document.querySelector('#doc-search')")
    assert is_focused
