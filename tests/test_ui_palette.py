import pytest
import re
from playwright.sync_api import Page, expect

def test_copy_button_interaction(page: Page):
    # Serve the docs using the dev server logic or just open the file
    # For simplicity, we can use the file path if it works, but app.js uses fetch
    # So we should probably run the dev server.

    import subprocess
    import time
    import os
    import signal

    # Start dev server
    process = subprocess.Popen(["python3", "scripts/dev.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Wait for server to start

    try:
        page.goto("http://127.0.0.1:4173/docs/library.html")

        # Grant clipboard permissions
        context = page.context
        context.grant_permissions(["clipboard-read", "clipboard-write"])

        # Find the first copy button
        copy_button = page.locator("[data-copy]").first

        # Initial state
        expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")
        original_text = copy_button.inner_text()

        # Click the button
        copy_button.click()

        # Feedback state
        expect(copy_button).to_have_text("Copied")
        expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")
        expect(copy_button).to_have_class(re.compile(r"is-valid"))

        # Wait for restoration (1400ms + some buffer)
        page.wait_for_timeout(2000)

        # Restored state
        expect(copy_button).to_have_text(original_text)
        expect(copy_button).to_have_attribute("aria-label", "Copy code to clipboard")
        expect(copy_button).not_to_have_class(re.compile(r"is-valid"))

        # Test rapid clicks
        copy_button.click()
        page.wait_for_timeout(500)
        copy_button.click()

        expect(copy_button).to_have_text("Copied")
        page.wait_for_timeout(2000)
        expect(copy_button).to_have_text(original_text)

    finally:
        os.kill(process.pid, signal.SIGTERM)

if __name__ == "__main__":
    pytest.main([__file__, "-s"])
