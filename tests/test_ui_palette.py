import pytest
import subprocess
import time
import socket
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    """Start the dev server for UI tests."""
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server to be ready
    max_retries = 30
    for _ in range(max_retries):
        try:
            with socket.create_connection(("127.0.0.1", 4173), timeout=1):
                break
        except (OSError, ConnectionRefusedError):
            time.sleep(0.5)
    else:
        process.terminate()
        stdout, stderr = process.communicate()
        raise RuntimeError(f"Server failed to start. stdout: {stdout}, stderr: {stderr}")

    yield
    process.terminate()

def test_copy_button_feedback(page: Page, context):
    """Verify that the copy button provides visual and accessible feedback."""
    # Grant clipboard permissions
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Target the first copy button
    copy_button = page.locator("[data-copy]").first

    # Initial state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click the button
    copy_button.click()

    # Feedback state
    expect(copy_button).to_have_text("Copied")
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration (1400ms timeout in app.js + some buffer)
    page.wait_for_timeout(2000)

    # Restored state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_copy_button_rapid_clicks(page: Page, context):
    """Verify that rapid clicks reset the restoration timeout."""
    context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("http://127.0.0.1:4173/docs/library.html")

    copy_button = page.locator("[data-copy]").first

    # Click multiple times
    copy_button.click()
    page.wait_for_timeout(500)
    copy_button.click()
    page.wait_for_timeout(500)
    copy_button.click()

    # At this point, it should still be in "Copied" state
    expect(copy_button).to_have_text("Copied")

    # Wait 1000ms. If timeout wasn't cleared, it would have reverted by now
    # (500 + 500 + 1000 = 2000ms total since first click, but only 1000ms since last click)
    page.wait_for_timeout(1000)
    expect(copy_button).to_have_text("Copied")

    # Wait more for it to finally revert
    page.wait_for_timeout(1000)
    expect(copy_button).to_have_text("Copy")
