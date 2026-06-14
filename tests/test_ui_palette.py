import pytest
import subprocess
import time
import socket
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    """Starts the dev server as a subprocess."""
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for the server to be ready
    retries = 10
    while retries > 0:
        try:
            with socket.create_connection(("127.0.0.1", 4173), timeout=1):
                break
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(0.5)
            retries -= 1

    if retries == 0:
        process.terminate()
        raise RuntimeError("Dev server failed to start")

    yield

    process.terminate()
    process.wait()

@pytest.fixture(autouse=True)
def clipboard_permissions(context):
    context.grant_permissions(["clipboard-read", "clipboard-write"])

def test_copy_button_feedback(page: Page):
    # Navigate to library page
    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Find the first copy button
    copy_button = page.locator("[data-copy]").first

    # Initial state check
    expect(copy_button).to_have_text(re.compile(r"Copy"))

    # Click to copy
    copy_button.click()

    # Feedback state check
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_class(re.compile(r"is-valid"))
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_copy_clipboard_content(page: Page):
    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Find the first code block and its copy button
    code_card = page.locator(".code-card").first
    copy_button = code_card.locator("[data-copy]")
    expected_text = code_card.locator("code").inner_text()

    copy_button.click()

    # Check clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

def test_command_card_copy(page: Page):
    # Navigate to index page
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Find the command card and its copy button
    command_card = page.locator(".command-card").first
    copy_button = command_card.locator("[data-copy]")
    expected_text = command_card.locator("code").inner_text()

    copy_button.click()

    # Feedback state
    expect(copy_button).to_have_text(re.compile(r"Copied"))

    # Clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

def test_rapid_clicks(page: Page):
    page.goto("http://127.0.0.1:4173/docs/library.html")
    copy_button = page.locator("[data-copy]").first

    # Rapid clicks
    copy_button.click()
    page.wait_for_timeout(200)
    copy_button.click()
    page.wait_for_timeout(200)
    copy_button.click()

    expect(copy_button).to_have_text(re.compile(r"Copied"))

    # Final restoration
    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
