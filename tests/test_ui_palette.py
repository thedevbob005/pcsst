import pytest
import subprocess
import time
import requests
import os
import signal
import re
from playwright.sync_api import expect

@pytest.fixture(scope="module")
def dev_server():
    process = subprocess.Popen(["python3", "scripts/dev.py"], preexec_fn=os.setsid)
    url = "http://127.0.0.1:4173"
    # Wait for server to be ready
    max_retries = 20
    for i in range(max_retries):
        try:
            requests.get(url)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    else:
        pytest.fail("Server did not start")

    yield url

    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def test_copy_button_rapid_click_fixed(page, dev_server):
    page.goto(f"{dev_server}/docs/library.html")

    # Grant clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # Target the first copy button
    copy_button = page.locator("[data-copy]").first

    # 1. Initial state
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")

    # 2. First click
    copy_button.click()
    expect(copy_button).to_have_text("Copied")
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # 3. Rapid second click (before 1400ms timeout)
    page.wait_for_timeout(500)
    copy_button.click()
    expect(copy_button).to_have_text("Copied")

    # 4. Wait for restoration timeout
    page.wait_for_timeout(2000)

    # It should restore to "Copy" now
    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_copy_button_aria_label_present(page, dev_server):
    page.goto(f"{dev_server}/docs/library.html")
    copy_button = page.locator("[data-copy]").first

    # Check if aria-label is correct
    aria_label = copy_button.get_attribute("aria-label")
    assert aria_label == "Copy code to clipboard"
