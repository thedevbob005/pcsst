import pytest
import time
import subprocess
import sys
import os
from pathlib import Path

PORT = 4174

@pytest.fixture(scope="module")
def server():
    # Start the dev server in a background process
    env = os.environ.copy()
    env["PORT"] = str(PORT)
    process = subprocess.Popen(
        [sys.executable, "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        cwd=Path(__file__).parent.parent
    )
    # Give the server a moment to start
    time.sleep(2)
    yield f"http://127.0.0.1:{PORT}"
    process.terminate()
    process.wait()

def test_copy_button_interaction(page, server):
    # Grant clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(f"{server}/docs/library.html")

    # Wait for the first copy button
    copy_button = page.locator("[data-copy]").first
    code_block = copy_button.locator("xpath=ancestor::div[contains(@class, 'code-card')]//code")

    expected_text = code_block.inner_text()

    # Initial state check
    assert copy_button.inner_text().strip() == "Copy"
    assert copy_button.get_attribute("aria-label") == "Copy code to clipboard"

    # Click the button
    copy_button.click()

    # Feedback state check
    assert copy_button.inner_text().strip() == "Copied"
    assert copy_button.get_attribute("aria-label") == "Copied to clipboard"
    assert "is-valid" in copy_button.get_attribute("class")

    # Check clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_text == expected_text

    # Wait for restoration
    page.wait_for_function(
        "btn => btn.innerText.trim() === 'Copy'",
        arg=copy_button.element_handle(),
        timeout=2000
    )

    # Restored state check
    assert copy_button.inner_text().strip() == "Copy"
    assert copy_button.get_attribute("aria-label") == "Copy code to clipboard"
    assert "is-valid" not in copy_button.get_attribute("class")

def test_copy_button_rapid_clicks(page, server):
    # Grant clipboard permissions to avoid "Copy failed" due to permission issues
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(f"{server}/docs/library.html")

    copy_button = page.locator("[data-copy]").first

    # Rapid clicks
    copy_button.click()
    time.sleep(0.1)
    copy_button.click()
    time.sleep(0.1)
    copy_button.click()

    # Should still be in feedback state
    assert copy_button.inner_text().strip() == "Copied"

    # Wait for restoration (longer than 1.4s)
    time.sleep(2)

    # Should have restored correctly
    assert copy_button.inner_text().strip() == "Copy"
