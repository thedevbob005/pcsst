import pytest
import subprocess
import time
import os
import signal
import re
from playwright.sync_api import expect

@pytest.fixture(scope="module")
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
    yield "http://127.0.0.1:4173"
    # Kill the server
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

def test_copy_button_library(dev_server, page):
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto(f"{dev_server}/docs/library.html")

    # Target the first copy button
    copy_button = page.locator("[data-copy]").first
    code_block = copy_button.locator("xpath=../..").locator("code")
    expected_text = code_block.inner_text()

    # Check initial state
    expect(copy_button).to_have_text(re.compile(r"Copy"))
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

    # Click copy
    copy_button.click()

    # Check feedback state
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_class(re.compile(r"is-valid"))
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Check clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_copy_button_command_card(dev_server, page):
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto(f"{dev_server}/docs/index.html")

    # Find the command card copy button
    copy_button = page.locator(".command-card [data-copy]")
    code_block = page.locator(".command-card code")
    expected_text = code_block.inner_text()

    # Click copy
    copy_button.click()

    # Check feedback
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Check clipboard
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

def test_copy_button_rapid_click(dev_server, page):
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto(f"{dev_server}/docs/library.html")

    copy_button = page.locator("[data-copy]").first

    # Rapid clicks
    copy_button.click()
    page.wait_for_timeout(100)
    copy_button.click()
    page.wait_for_timeout(100)
    copy_button.click()

    expect(copy_button).to_have_text(re.compile(r"Copied"))

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
