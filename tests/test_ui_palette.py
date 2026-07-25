import os
import socket
import subprocess
import time
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

@pytest.fixture(scope="module")
def dev_server():
    port = 4173
    env = os.environ.copy()
    env["PORT"] = str(port)
    proc = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        cwd=str(ROOT_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for port to be open
    for _ in range(50):
        if is_port_open(port):
            break
        time.sleep(0.1)
    else:
        proc.terminate()
        proc.wait()
        raise RuntimeError("Failed to start dev server on port 4173")

    yield f"http://127.0.0.1:{port}"

    proc.terminate()
    proc.wait()

def test_copy_buttons_command_card(dev_server, page):
    # Grant clipboard permissions
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    page.goto(f"{dev_server}/docs/getting-started.html")

    # Find the Copy button on the command-card
    copy_btn = page.locator(".command-card button[data-copy]").first

    # Verify initial state
    expect_btn_aria = copy_btn.get_attribute("aria-label")
    assert expect_btn_aria == "Copy commands to clipboard"
    assert copy_btn.inner_text().strip() == "Copy"

    # Click the Copy button
    copy_btn.click()

    # Verify feedback state
    assert copy_btn.inner_text().strip() == "Copied"
    assert copy_btn.get_attribute("aria-label") == "Copied to clipboard"
    assert "is-valid" in (copy_btn.get_attribute("class") or "")

    # Verify clipboard content
    clipboard_text = page.evaluate("navigator.clipboard.readText()")
    assert "python3 scripts/build.py" in clipboard_text

    # Wait for feedback state to restore (1400ms timeout)
    page.wait_for_timeout(1500)

    assert copy_btn.inner_text().strip() == "Copy"
    assert copy_btn.get_attribute("aria-label") == "Copy commands to clipboard"
    assert "is-valid" not in (copy_btn.get_attribute("class") or "")
