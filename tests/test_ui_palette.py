import subprocess
import time
import socket
import pytest
from playwright.sync_api import expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start dev server
    proc = subprocess.Popen(["python3", "scripts/dev.py"])

    # Wait for port 4173 to open
    for _ in range(30):
        try:
            with socket.create_connection(("127.0.0.1", 4173), timeout=0.1):
                break
        except (OSError, ConnectionRefusedError):
            time.sleep(0.1)
    else:
        proc.terminate()
        proc.wait()
        raise RuntimeError("Failed to start dev server on port 4173")

    yield

    proc.terminate()
    proc.wait()

def test_search_shortcut_indicator(page):
    # Navigate to the search page
    page.goto("http://127.0.0.1:4173/docs/search.html")

    # Check that indicator is visible
    indicator = page.locator("[data-search-shortcut-indicator]")
    expect(indicator).to_be_visible()

    # Verify indicator has a valid value (e.g. ⌘K or Ctrl+K)
    text = indicator.text_content()
    assert text in ("⌘K", "Ctrl+K")
