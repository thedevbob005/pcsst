import sys
import subprocess
import time
import socket
import pytest
import re
from pathlib import Path
from playwright.sync_api import Page, expect

def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start scripts/dev.py on port 4173
    cmd = [sys.executable, str(Path(__file__).resolve().parent.parent / "scripts" / "dev.py")]
    proc = subprocess.Popen(cmd)

    # Wait for the server to be ready
    for _ in range(50):
        if is_port_open(4173):
            break
        time.sleep(0.1)
    else:
        proc.terminate()
        proc.wait()
        raise RuntimeError("Server failed to start on port 4173")

    yield proc

    proc.terminate()
    proc.wait()

def test_copy_button_interaction(page: Page):
    # Mock clipboard API
    page.add_init_script("navigator.clipboard.writeText = async (text) => { window.__copiedText = text; };")

    # Navigate to index.html
    page.goto("http://127.0.0.1:4173/docs/index.html")

    # Find the Copy button on the command card
    copy_btn = page.locator(".command-card button[data-copy]").first
    expect(copy_btn).to_be_visible()

    # Check original properties
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click the Copy button
    copy_btn.click()

    # Verify feedback state
    expect(copy_btn).to_have_text(re.compile(r"Copied"))
    expect(copy_btn).to_have_attribute("aria-label", "Copied to clipboard")
    expect(copy_btn).to_have_class(re.compile(r"is-valid"))

    # Wait and verify that it restores
    page.wait_for_timeout(1500)
    expect(copy_btn).to_have_text(re.compile(r"Copy"))
    expect(copy_btn).to_have_attribute("aria-label", "Copy commands to clipboard")

    # The .is-valid class should be removed
    expect(copy_btn).to_have_class(re.compile(r"button--sm"))
    assert "is-valid" not in (copy_btn.get_attribute("class") or "")
