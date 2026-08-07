import subprocess
import time
import socket
import os
import pytest
from playwright.sync_api import Page, expect

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start dev.py as a subprocess on port 4173
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"PORT": "4173", **os.environ}
    )
    # Wait for the server to start
    for _ in range(50):
        if is_port_open(4173):
            break
        time.sleep(0.1)

    yield process

    # Terminate process on teardown
    process.terminate()
    process.wait()

def test_homepage_command_card_copy(page: Page):
    # Mock clipboard API using Object.defineProperty to bypass read-only restrictions
    page.add_init_script("""
        Object.defineProperty(navigator, 'clipboard', {
            value: {
                writeText: async (text) => {
                    window.__copiedText = text;
                }
            },
            configurable: true
        });
    """)

    # Go to homepage with full path to ensure relative paths like app.js resolve correctly
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Locate the copy button on the command card
    btn = page.locator(".command-card button[data-copy]").first
    expect(btn).to_be_visible()

    # Check initial aria-label
    expect(btn).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click the copy button
    btn.click()

    # Verify text was copied correctly (trimmed)
    copied_text = page.evaluate("window.__copiedText")
    assert copied_text is not None
    assert "python3 scripts/build.py" in copied_text
    assert copied_text.strip() == copied_text

    # Check feedback states
    expect(btn).to_have_text("Copied")
    expect(btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(btn).to_have_class(compile_class_regex("is-valid"))

    # Wait for feedback timeout (1400ms) to clear
    page.wait_for_timeout(1600)

    # Check reverted state
    expect(btn).to_have_text("Copy")
    expect(btn).to_have_attribute("aria-label", "Copy commands to clipboard")
    expect(btn).not_to_have_class(compile_class_regex("is-valid"))

def test_getting_started_code_card_copy(page: Page):
    # Mock clipboard API using Object.defineProperty
    page.add_init_script("""
        Object.defineProperty(navigator, 'clipboard', {
            value: {
                writeText: async (text) => {
                    window.__copiedText = text;
                }
            },
            configurable: true
        });
    """)

    # Go to getting-started page
    page.goto("http://127.0.0.1:4173/docs/getting-started.html")

    # Locate copy button on code card
    btn = page.locator(".code-card button[data-copy]").first
    expect(btn).to_be_visible()

    # Check initial aria-label
    expect(btn).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click copy
    btn.click()

    # Verify clipboard content
    copied_text = page.evaluate("window.__copiedText")
    assert copied_text is not None
    assert "<div class=" in copied_text

    # Check feedback states
    expect(btn).to_have_text("Copied")
    expect(btn).to_have_class(compile_class_regex("is-valid"))

    # Wait for feedback timeout
    page.wait_for_timeout(1600)

    # Check reverted state
    expect(btn).to_have_text("Copy")
    expect(btn).not_to_have_class(compile_class_regex("is-valid"))

def compile_class_regex(class_name):
    import re
    return re.compile(rf"\b{class_name}\b")
