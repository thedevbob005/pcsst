import pytest
import subprocess
import time
import requests
from playwright.sync_api import Page, expect
import re

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    """Starts the dev server as a subprocess."""
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for the server to be ready
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://127.0.0.1:4173/docs/index.html")
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    else:
        process.terminate()
        pytest.fail("Dev server failed to start")

    yield

    process.terminate()
    process.wait()

def test_command_card_copy(page: Page, context):
    context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Find the copy button in the command card
    copy_button = page.locator(".command-card [data-copy]").first

    # Click it
    copy_button.click()

    # Check feedback
    expect(copy_button).to_have_text(re.compile(r"Copied"))
    expect(copy_button).to_have_class(re.compile(r"is-valid"))

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert "python3 scripts/build.py" in clipboard_text

    # Wait for restoration
    page.wait_for_timeout(2000)
    expect(copy_button).to_have_text(re.compile(r"Copy"))
    expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

def test_code_card_copy(page: Page, context):
    context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("http://127.0.0.1:4173/docs/library.html")

    # Find the first copy button in a code card
    copy_button = page.locator(".code-card [data-copy]").first

    # Click it
    copy_button.click()

    # Check feedback
    expect(copy_button).to_have_text(re.compile(r"Copied"))

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert '<link rel="stylesheet" href="dist/pcsst.css" />' in clipboard_text
