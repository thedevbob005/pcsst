import pytest
import re
from playwright.sync_api import Page, expect
import subprocess
import time
import os
import signal

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start the dev server
    proc = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    # Wait for server to be ready
    time.sleep(2)
    yield
    # Kill the server process group
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

def test_copy_button_feedback(page: Page):
    # Enable clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Find the first copy button
    copy_button = page.locator("[data-copy]").first

    # Check initial state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click the button
    copy_button.click()

    # Check "Copied" state
    expect(copy_button).to_have_text("Copied")
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration (1400ms + buffer)
    page.wait_for_timeout(2000)

    # Check restored state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_copy_button_rapid_click(page: Page):
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto("http://127.0.0.1:4173/docs/library.html")
    copy_button = page.locator("[data-copy]").first

    # Rapid clicks
    copy_button.click()
    page.wait_for_timeout(500)
    copy_button.click()
    page.wait_for_timeout(500)
    copy_button.click()

    # Should still be in "Copied" state
    expect(copy_button).to_have_text("Copied")

    # Wait for restoration from last click
    page.wait_for_timeout(2000)

    # Should be restored
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")
