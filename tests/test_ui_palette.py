import pytest
import subprocess
import time
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    """Starts the local development server for the duration of the test module."""
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Wait for the server to be ready
    time.sleep(2)
    yield
    process.terminate()

def test_copy_button_interaction(page: Page):
    # Grant clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # Navigate to the docs root (which redirects to /docs/index.html)
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Find a command card copy button
    copy_button = page.locator(".command-card [data-copy]").first

    # Check initial state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click the button
    copy_button.click()

    # Check feedback state
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration
    page.wait_for_timeout(2000)

    # Check restored state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_library_copy_buttons(page: Page):
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Find the first code-card copy button
    copy_button = page.locator(".code-card [data-copy]").first

    # Check initial state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click and verify feedback
    copy_button.click()
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Verify rapid clicks (state should stay 'Copied' and then restore correctly)
    copy_button.click()
    page.wait_for_timeout(500)
    copy_button.click()

    expect(copy_button).to_have_text(re.compile(r"Copied"))

    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))
