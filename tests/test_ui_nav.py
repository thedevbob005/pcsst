import re
import subprocess
import time
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def server():
    proc = subprocess.Popen(["python3", "scripts/dev.py", "--port", "4173"])
    time.sleep(1)
    yield proc
    proc.terminate()
    proc.wait()

def test_mobile_nav_escape_key(page: Page):
    page.set_viewport_size({"width": 600, "height": 800})
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Toggle button and menu
    toggle = page.locator("[data-nav-toggle]")
    menu = page.locator("[data-site-menu]")

    # Initially, menu is not open and aria-expanded is false
    expect(toggle).to_have_attribute("aria-expanded", "false")
    expect(menu).not_to_have_class(re.compile(r"\bis-open\b"))

    # Click toggle to open menu
    toggle.click()
    expect(toggle).to_have_attribute("aria-expanded", "true")
    expect(menu).to_have_class(re.compile(r"\bis-open\b"))

    # Press Escape key
    page.keyboard.press("Escape")

    # Menu should be closed, aria-expanded false, and focus returned to toggle
    expect(toggle).to_have_attribute("aria-expanded", "false")
    expect(menu).not_to_have_class(re.compile(r"\bis-open\b"))

    is_toggle_focused = page.evaluate("document.activeElement === document.querySelector('[data-nav-toggle]')")
    assert is_toggle_focused, "Nav toggle button should have focus after pressing Escape"
