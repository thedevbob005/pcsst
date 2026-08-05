import pytest
import subprocess
import time
import socket
import re
from playwright.sync_api import Page, expect

def wait_for_port(port, host="127.0.0.1", timeout=5.0):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except (socket.timeout, ConnectionRefusedError):
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.1)

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    proc = subprocess.Popen(["python3", "scripts/dev.py"])
    if not wait_for_port(4173):
        proc.terminate()
        raise RuntimeError("Dev server failed to start on port 4173")
    yield
    proc.terminate()
    proc.wait()

def test_command_card_copy_button(page: Page):
    page.add_init_script("navigator.clipboard.writeText = async () => {};")
    page.goto("http://localhost:4173/docs/index.html")

    container = page.locator(".command-card").first
    copy_button = container.locator("button[data-copy]")

    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    copy_button.click()

    expect(copy_button).to_have_text("Copied")
    expect(copy_button).to_have_attribute("aria-label", "Copied to clipboard")
    expect(container).to_have_class(re.compile(r"is-valid"))

    page.wait_for_timeout(1600)

    expect(copy_button).to_have_text("Copy")
    expect(copy_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Use to_have_class with negation if supported, or directly verify class list
    # Let's ensure 'is-valid' is not present by matching against a regex that doesn't contain it
    # or using Page's evaluate/attribute checks
    classes = container.get_attribute("class") or ""
    assert "is-valid" not in classes.split()
