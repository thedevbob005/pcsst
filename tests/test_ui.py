import pytest
from playwright.sync_api import Page, expect

def test_copy_button_feedback(page: Page):
    # Start the dev server
    import subprocess
    import time
    import os
    import signal

    process = subprocess.Popen(["python3", "scripts/dev.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Wait for server to start

    try:
        page.goto("http://127.0.0.1:4173/docs/library.html")

        # Grant clipboard permissions
        context = page.context
        context.grant_permissions(["clipboard-read", "clipboard-write"])

        copy_button = page.locator("[data-copy]").first

        # Check initial state
        expect(copy_button).to_be_visible()
        expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")

        # Click the button
        copy_button.click()

        # Check "Copied" state
        expect(copy_button).to_have_text("Copied")
        expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")

        # Wait for restoration
        page.wait_for_timeout(2000)

        # Check restored state
        expect(copy_button).to_have_text("Copy")
        expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")

    finally:
        os.kill(process.pid, signal.SIGTERM)

if __name__ == "__main__":
    pytest.main([__file__])
