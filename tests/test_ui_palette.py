import sys
import subprocess
import time
import socket
import re
import pytest
from playwright.sync_api import expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    proc = subprocess.Popen([sys.executable, "scripts/dev.py"])

    start_time = time.time()
    while time.time() - start_time < 5:
        try:
            with socket.create_connection(("127.0.0.1", 4173), timeout=1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        proc.terminate()
        proc.wait()
        raise RuntimeError("Local development server failed to start on port 4173.")

    yield

    proc.terminate()
    proc.wait()

def test_command_card_copy_button(page):
    # Mock the clipboard API
    page.add_init_script("navigator.clipboard.writeText = async () => {};")

    # Navigate to the index.html page (relative path resolving needs /docs/ base)
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Locate the copy button in the command card by its attributes (stable CSS selector)
    btn = page.locator(".command-card button[data-copy]").first

    # Verify its initial state
    expect(btn).to_be_visible()
    expect(btn).to_have_attribute("aria-label", "Copy commands to clipboard")
    expect(btn).to_have_text(re.compile(r"Copy"))

    # Click the button
    btn.click()

    # Verify the interactive feedback state (with is-valid class)
    expect(btn).to_have_class(re.compile(r"is-valid"))
    expect(btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(btn).to_have_text(re.compile(r"Copied"))

    # Wait for the feedback state to reset (1400ms timeout)
    page.wait_for_timeout(1600)

    # Verify the state has reverted back
    expect(btn).not_to_have_class(re.compile(r"is-valid"))
    expect(btn).to_have_attribute("aria-label", "Copy commands to clipboard")
    expect(btn).to_have_text(re.compile(r"Copy"))
