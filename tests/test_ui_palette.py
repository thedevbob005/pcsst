import pytest
import re
import subprocess
import time

try:
    from playwright.sync_api import expect
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not PLAYWRIGHT_AVAILABLE,
    reason="playwright and pytest-playwright are required for UI tests"
)

@pytest.fixture(scope="module")
def dev_server():
    process = subprocess.Popen(["python3", "scripts/dev.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for server to be ready
    time.sleep(1)
    yield "http://127.0.0.1:4173"
    process.terminate()

def test_copy_button_index(page, dev_server):
    page.goto(f"{dev_server}/docs/index.html")

    # Check for the copy button in command-card
    copy_button = page.locator(".command-card [data-copy]")
    expect(copy_button).to_be_visible()
    expect(copy_button).to_have_text(re.compile(r"Copy"))
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Give clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # Click copy button
    copy_button.click()

    # Check feedback state
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Wait for timeout to restore state
    page.wait_for_timeout(1600)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_copy_button_library(page, dev_server):
    # Give clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(f"{dev_server}/docs/library.html")

    # Get first copy button (in code-card)
    copy_button = page.locator(".code-card [data-copy]").first
    expect(copy_button).to_be_visible()

    # Click copy button
    copy_button.click()

    # Check feedback state
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Wait for timeout to restore state
    page.wait_for_timeout(1600)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
