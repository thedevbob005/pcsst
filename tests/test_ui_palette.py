import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(autouse=True)
def setup_clipboard_mock(page: Page):
    # Mock clipboard API in the browser context
    page.add_init_script("navigator.clipboard.writeText = async () => {};")

def test_copy_button_interaction(page: Page):
    # Open the documentation overview page
    page.goto("http://localhost:4173/docs/index.html")

    # Target the copy button in the command card
    copy_button = page.locator(".command-card button[data-copy]")

    # Verify initial state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click the copy button to trigger clipboard copy
    copy_button.click()

    # Assert visual confirmation class and text/aria label update
    expect(copy_button).to_have_class(re.compile(r"is-valid"))
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for the feedback state to restore
    page.wait_for_timeout(1600)

    # Assert restoration back to initial state
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")
