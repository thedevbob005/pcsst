import sys
import os
import subprocess
import time
import socket
import re
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

# Add scripts directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))

def wait_for_port(port: int, host: str = "127.0.0.1", timeout: float = 5.0) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(0.1)
    return False

@pytest.fixture(scope="module")
def dev_server():
    # Start the development server using the python interpreter running pytest
    python_exe = sys.executable
    server_path = str(Path(__file__).resolve().parent.parent / "scripts" / "dev.py")

    port = 4173

    process = subprocess.Popen(
        [python_exe, server_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "PORT": str(port)}
    )

    # Wait for server to become responsive
    if not wait_for_port(port):
        process.terminate()
        raise RuntimeError(f"Development server failed to start on port {port}")

    yield f"http://127.0.0.1:{port}"

    process.terminate()
    process.wait()

def test_copy_button_interaction(dev_server, page: Page):
    # Mock the navigator.clipboard.writeText API as it's typically blocked in headless browsers
    page.add_init_script("navigator.clipboard.writeText = async () => {};")

    page.goto(f"{dev_server}/docs/index.html")

    # Locate our command card's copy button
    copy_btn = page.locator(".command-card button[data-copy]")
    expect(copy_btn).to_be_visible()

    # Check initial state
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click copy button
    copy_btn.click()

    # Assert successful copy visual feedback
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_btn).to_have_class(re.compile(r"is-valid"))

    # Wait for the feedback state to restore (timeout is 1400ms, let's wait 1600ms)
    page.wait_for_timeout(1600)

    # Assert state is fully restored
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Check that is-valid is removed
    has_is_valid = False
    classes = copy_btn.get_attribute("class") or ""
    if "is-valid" in classes:
        has_is_valid = True
    assert not has_is_valid
