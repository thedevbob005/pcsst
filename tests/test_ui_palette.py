import pytest
import subprocess
import time
import re
from playwright.sync_api import expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    process = subprocess.Popen(["python3", "scripts/dev.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for server to start
    yield
    process.terminate()

def test_copy_buttons_feedback(page):
    # Enable clipboard access
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    pages_to_test = ["/docs/index.html", "/docs/getting-started.html", "/docs/changelog.html"]

    for doc_path in pages_to_test:
        page.goto(f"http://127.0.0.1:4173{doc_path}")

        # Find all copy buttons (including new ones in command-cards)
        copy_buttons = page.locator("[data-copy]")
        count = copy_buttons.count()
        assert count > 0, f"No copy buttons found on {doc_path}"

        for i in range(count):
            button = copy_buttons.nth(i)

            # Get original text
            original_text = button.inner_text().strip()

            # Click the button
            button.click()

            # Verify visual feedback
            expect(button).to_have_text(re.compile(r"Copied"))

            # Verify clipboard content (checking first button only to avoid race/complexities)
            if i == 0:
                # Give a small moment for clipboard write
                time.sleep(0.5)
                clipboard_content = page.evaluate("navigator.clipboard.readText()")
                assert clipboard_content.strip() != "", f"Clipboard is empty after clicking button on {doc_path}"

            # Wait for restoration
            time.sleep(1.5)
            expect(button).to_have_text(original_text)
