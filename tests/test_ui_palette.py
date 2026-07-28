import re
import socket
import subprocess
import time
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start the local development server as a subprocess
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for the server to be ready on port 4173
    port = 4173
    retries = 30
    for _ in range(retries):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                break
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(0.1)
    else:
        process.terminate()
        raise RuntimeError(f"Server failed to start on port {port}")

    yield

    process.terminate()
    process.wait()

def test_copy_button_code_card(page: Page):
    # Mock clipboard API because headless browsers lack clipboard permissions
    page.add_init_script("navigator.clipboard.writeText = async () => {};")

    # Navigate to the getting started page
    page.goto("http://127.0.0.1:4173/docs/getting-started.html")

    # Locate the copy button inside the code-card
    button = page.locator(".code-card button[data-copy]")
    expect(button).to_be_visible()
    expect(button).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click the copy button
    button.click()

    # Check updated text and class and aria-label
    expect(button).to_have_text(re.compile(r"Copied"))
    expect(button).to_have_class(re.compile(r"is-valid"))
    expect(button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for the feedback state to restore (1400ms defined timeout + margin)
    page.wait_for_timeout(2000)

    # Verify restoration
    expect(button).to_have_text(re.compile(r"Copy"))
    # Verify that class 'is-valid' is not present
    class_name = button.get_attribute("class") or ""
    assert "is-valid" not in class_name
    expect(button).to_have_attribute("aria-label", "Copy code to clipboard")

def test_copy_button_command_card(page: Page):
    # Mock clipboard API because headless browsers lack clipboard permissions
    page.add_init_script("navigator.clipboard.writeText = async () => {};")

    # Navigate to the getting started page
    page.goto("http://127.0.0.1:4173/docs/getting-started.html")

    # Locate the copy button inside the command-card
    button = page.locator(".command-card button[data-copy]")
    expect(button).to_be_visible()
    expect(button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click the copy button
    button.click()

    # Check updated text and class and aria-label
    expect(button).to_have_text(re.compile(r"Copied"))
    expect(button).to_have_class(re.compile(r"is-valid"))
    expect(button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for the feedback state to restore
    page.wait_for_timeout(2000)

    # Verify restoration
    expect(button).to_have_text(re.compile(r"Copy"))
    # Verify that class 'is-valid' is not present
    class_name = button.get_attribute("class") or ""
    assert "is-valid" not in class_name
    expect(button).to_have_attribute("aria-label", "Copy commands to clipboard")
