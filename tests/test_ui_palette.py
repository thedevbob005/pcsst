import subprocess
import time
import socket
import re
import pytest
from playwright.sync_api import expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start dev server
    proc = subprocess.Popen(["python3", "scripts/dev.py"])

    # Wait for port 4173 to open
    for _ in range(30):
        try:
            with socket.create_connection(("127.0.0.1", 4173), timeout=0.1):
                break
        except (OSError, ConnectionRefusedError):
            time.sleep(0.1)
    else:
        proc.terminate()
        proc.wait()
        raise RuntimeError("Failed to start dev server on port 4173")

    yield

    proc.terminate()
    proc.wait()

def test_getting_started_copy_buttons(page):
    # Navigate to the getting started page on our running dev server
    page.goto("http://localhost:4173/docs/getting-started.html")

    # Give browser context the proper clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # 1. Verify Command Card Copy Button
    command_button = page.locator('.command-card [data-copy]')
    expect(command_button).to_be_visible()
    expect(command_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click and verify feedback state
    command_button.click()
    expect(command_button).to_have_text(re.compile(r"Copied"))
    expect(command_button).to_have_class(re.compile(r"is-valid"))
    expect(command_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for state restoration (1400ms timeout) and verify restored state
    page.wait_for_timeout(1600)
    expect(command_button).to_have_text(re.compile(r"Copy"))
    expect(command_button).not_to_have_class(re.compile(r"is-valid"))
    expect(command_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # 2. Verify Standard Code Card Copy Button
    code_button = page.locator('.code-card [data-copy]')
    expect(code_button).to_be_visible()
    expect(code_button).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click and verify feedback state
    code_button.click()
    expect(code_button).to_have_text(re.compile(r"Copied"))
    expect(code_button).to_have_class(re.compile(r"is-valid"))
    expect(code_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait and verify restored state
    page.wait_for_timeout(1600)
    expect(code_button).to_have_text(re.compile(r"Copy"))
    expect(code_button).not_to_have_class(re.compile(r"is-valid"))
    expect(code_button).to_have_attribute("aria-label", "Copy code to clipboard")
