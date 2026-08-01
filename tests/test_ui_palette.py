import subprocess
import time
import socket
import pytest
import re
from playwright.sync_api import Page, expect

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

@pytest.fixture(scope="session", autouse=True)
def dev_server():
    proc = subprocess.Popen(["python3", "scripts/dev.py"])
    start_time = time.time()
    success = False
    while time.time() - start_time < 5:
        if is_port_open(4173):
            success = True
            break
        time.sleep(0.1)
    if not success:
        proc.terminate()
        proc.wait()
        raise RuntimeError("Development server failed to start on port 4173 within timeout.")
    yield
    proc.terminate()
    proc.wait()

def test_copy_button_interaction(page: Page):
    # Print console logs and page errors
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGE ERROR: {err.message}"))

    # Define clipboard mock properly
    page.add_init_script("""
        Object.defineProperty(navigator, 'clipboard', {
            value: {
                writeText: async (text) => {
                    console.log('Mocked writeText called with:', text);
                }
            },
            configurable: true
        });
    """)

    # Go to index page
    page.goto("http://localhost:4173/docs/index.html")

    # Find the command card copy button using stable CSS selector
    copy_btn = page.locator(".command-card button[data-copy]").first
    expect(copy_btn).to_be_visible()

    # Verify initial state
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click the copy button
    copy_btn.click()

    # Verify feedback state using .*is-valid.*
    expect(copy_btn).to_have_class(re.compile(r".*is-valid.*"))
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for the restore timeout (1400ms)
    page.wait_for_timeout(1600)

    # Verify restoration state
    expect(copy_btn).not_to_have_class(re.compile(r".*is-valid.*"))
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")
