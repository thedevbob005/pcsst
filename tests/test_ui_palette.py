import pytest
import subprocess
import time
import os
import signal
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start the dev server
    proc = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    # Wait for the server to be ready
    time.sleep(2)
    yield
    # Kill the server process group
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

@pytest.fixture(autouse=True)
def setup_context(context):
    context.grant_permissions(["clipboard-read", "clipboard-write"])

def test_copy_button_code_card(page: Page):
    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Target the first copy button
    copy_btn = page.locator("[data-copy]").first
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click to copy
    copy_btn.click()

    # Check feedback state
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_btn).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy code to clipboard")
    expect(copy_btn).not_to_have_class(re.compile(r"is-valid"))

def test_copy_button_command_card(page: Page):
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Target the command card copy button
    copy_btn = page.locator(".command-card [data-copy]")
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click to copy
    copy_btn.click()

    # Check feedback state
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_btn).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")
    expect(copy_btn).not_to_have_class(re.compile(r"is-valid"))

def test_copy_button_rapid_clicks(page: Page):
    page.goto("http://127.0.0.1:4173/docs/library.html")
    copy_btn = page.locator("[data-copy]").first

    # Rapid clicks
    copy_btn.click()
    page.wait_for_timeout(500)
    copy_btn.click()
    page.wait_for_timeout(500)
    copy_btn.click()

    expect(copy_btn).to_have_text(re.compile(r"Copied"))

    # Wait for final restoration
    page.wait_for_timeout(2000)
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
