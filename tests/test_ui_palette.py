import pytest
import re
import subprocess
import time
from playwright.sync_api import Page, expect, BrowserContext

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start dev server
    proc = subprocess.Popen(["python3", "scripts/dev.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Wait for server to start
    yield
    proc.terminate()

@pytest.fixture(autouse=True)
def clipboard_permissions(context: BrowserContext):
    context.grant_permissions(["clipboard-read", "clipboard-write"])

def test_copy_button_feedback(page: Page):
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Find a command card
    command_card = page.locator(".command-card").first
    copy_button = command_card.locator("[data-copy]")
    code_block = command_card.locator("code")

    expected_text = code_block.inner_text().strip()

    # Initial state
    expect(copy_button).to_have_text("Copy")

    # Click copy
    copy_button.click()

    # Feedback state
    expect(copy_button).to_have_text("Copied")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

    # Wait for restoration
    page.wait_for_timeout(2000)

    # Restored state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))
