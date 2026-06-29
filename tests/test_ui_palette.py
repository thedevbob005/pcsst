import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def setup_server():
    # Server is already running from previous step
    yield

def test_copy_button_interaction(page: Page, context):
    context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Target the first copy button (Get Started section)
    copy_btn = page.locator("[data-copy]").first

    # Check initial state (should NOT have aria-label according to current simplified plan)
    expect(copy_btn).not_to_have_attribute("aria-label", re.compile(r".+"))

    # Click and check feedback state
    copy_btn.click()
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_class(re.compile(r"is-valid"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).not_to_have_class(re.compile(r"is-valid"))
    # Should restore to no aria-label
    expect(copy_btn).not_to_have_attribute("aria-label", re.compile(r".+"))
