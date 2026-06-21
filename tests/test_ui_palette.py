import pytest
import re
import subprocess
import time
import os
import sys
from playwright.sync_api import Page, expect, BrowserContext

@pytest.fixture(scope="module")
def dev_server():
    # Start dev server from repository root
    proc = subprocess.Popen(["python3", "scripts/dev.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Wait for server to start on port 4173
    time.sleep(2)
    yield
    proc.terminate()

@pytest.fixture
def clipboard_permissions(context: BrowserContext):
    context.grant_permissions(["clipboard-read", "clipboard-write"])

def test_command_card_copy_interaction(page: Page, dev_server, clipboard_permissions):
    # Navigate to overview page where command cards are present
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Locate the first command card copy button
    command_card = page.locator(".command-card").first
    copy_button = command_card.locator("[data-copy]")
    code_block = command_card.locator("code")

    expected_text = code_block.inner_text().strip()

    # Initial state verification
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Trigger copy
    copy_button.click()

    # Immediate feedback verification
    expect(copy_button).to_have_text("Copied")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

    # Verify restoration after timeout
    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")

def test_library_code_copy_interaction(page: Page, dev_server, clipboard_permissions):
    # Navigate to library reference
    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Locate the first code card copy button
    code_card = page.locator(".code-card").first
    copy_button = code_card.locator("[data-copy]")
    code_block = code_card.locator("code")

    expected_text = code_block.inner_text().strip()

    # Trigger copy
    copy_button.click()

    # Verify feedback
    expect(copy_button).to_have_text("Copied")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Verify clipboard
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text
