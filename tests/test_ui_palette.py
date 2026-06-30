import pytest
import subprocess
import time
import os
import signal
import re
from playwright.sync_api import expect

@pytest.fixture(scope="module")
def dev_server():
    # Start dev server
    proc = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid
    )
    # Wait for server to be ready
    time.sleep(2)
    yield "http://127.0.0.1:4173"
    # Kill server
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

def test_copy_button_feedback(dev_server, page):
    # Grant clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(f"{dev_server}/docs/index.html")

    # Test command card copy button
    copy_btn = page.locator(".command-card [data-copy]").first
    original_text = copy_btn.inner_text()
    original_aria = copy_btn.get_attribute("aria-label")

    # Click copy button
    copy_btn.click()

    # Check feedback state
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_btn).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration
    time.sleep(2)

    # Check restored state
    expect(copy_btn).to_have_text(original_text)
    expect(copy_btn).to_have_attribute("aria-label", original_aria)
    expect(copy_btn).not_to_have_class(re.compile(r"is-valid"))

def test_library_copy_button_feedback(dev_server, page):
    # Grant clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(f"{dev_server}/docs/library.html")

    # Test code card copy button
    copy_btn = page.locator(".code-card [data-copy]").first
    original_text = copy_btn.inner_text()
    original_aria = copy_btn.get_attribute("aria-label")

    # Click copy button
    copy_btn.click()

    # Check feedback state
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_btn).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration
    time.sleep(2)

    # Check restored state
    expect(copy_btn).to_have_text(original_text)
    expect(copy_btn).to_have_attribute("aria-label", original_aria)
    expect(copy_btn).not_to_have_class(re.compile(r"is-valid"))
