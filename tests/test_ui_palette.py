import os
import subprocess
import time
import socket
import pytest
from playwright.sync_api import Page

def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

@pytest.fixture(scope="module")
def dev_server():
    port = 4173
    # Start the server
    proc = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        env={**os.environ, "PORT": str(port)},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for the server to be ready
    start_time = time.time()
    while time.time() - start_time < 5:
        if is_port_open(port):
            break
        time.sleep(0.1)
    else:
        proc.kill()
        raise RuntimeError("Dev server failed to start within 5 seconds")

    yield f"http://127.0.0.1:{port}"

    proc.terminate()
    proc.wait()

def test_copy_button_interaction(dev_server, page: Page):
    # Mock navigator.clipboard
    page.add_init_script(
        """
        Object.defineProperty(navigator, 'clipboard', {
            value: {
                writeText: async (text) => {
                    window.__copiedText = text;
                }
            },
            configurable: true
        });
        """
    )

    # Navigate to the index.html page
    page.goto(f"{dev_server}/docs/index.html")

    # Locate the copy button on the command card
    btn = page.locator(".command-card button[data-copy]").first

    # Verify initial state
    assert btn.text_content().strip() == "Copy"
    assert btn.get_attribute("aria-label") == "Copy commands to clipboard"
    assert "is-valid" not in btn.evaluate("el => el.className")
    assert "is-invalid" not in btn.evaluate("el => el.className")

    # Click the copy button
    btn.click()

    # Verify copied text in window
    copied_text = page.evaluate("window.__copiedText")
    assert "python3 scripts/build.py" in copied_text

    # Verify success feedback states
    assert btn.text_content().strip() == "Copied"
    assert btn.get_attribute("aria-label") == "Copied to clipboard"
    assert "is-valid" in btn.evaluate("el => el.className")

    # Wait for recovery (1400ms feedback timeout)
    page.wait_for_timeout(1600)

    # Verify restored states
    assert btn.text_content().strip() == "Copy"
    assert btn.get_attribute("aria-label") == "Copy commands to clipboard"
    assert "is-valid" not in btn.evaluate("el => el.className")
