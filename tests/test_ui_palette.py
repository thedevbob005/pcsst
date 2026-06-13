import subprocess
import time
import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    """Starts the dev server for UI testing."""
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Wait for the server to be ready
    time.sleep(2)
    yield
    process.terminate()

def test_copy_button_interaction(page: Page):
    # Enable clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # Test on library.html (original code-card)
    page.goto("http://127.0.0.1:4173/docs/library.html")

    copy_button = page.locator("[data-copy]").first
    code_block = copy_button.locator("xpath=ancestor::*[@class='code-card']//code")

    expected_text = code_block.inner_text()

    # Click and verify feedback
    copy_button.click()
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

    # Verify rapid click behavior
    copy_button.click()
    copy_button.click()
    expect(copy_button).to_have_text(re.compile(r"Copied"))

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_command_card_copy_button(page: Page):
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # Test on index.html (new command-card)
    page.goto("http://127.0.0.1:4173/docs/index.html")

    copy_button = page.locator(".command-card [data-copy]").first
    code_block = copy_button.locator("xpath=ancestor::*[@class='command-card']//code")

    expected_text = code_block.inner_text()

    # Click and verify feedback
    copy_button.click()
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text
