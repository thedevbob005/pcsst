import sys
import os
import subprocess
import time
import socket
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def dev_server():
    # Find a free port or use 4173
    port = "4173"
    env = os.environ.copy()
    env["PORT"] = port

    # Start dev.py as subprocess
    proc = subprocess.Popen(
        [sys.executable, "scripts/dev.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for the server to be up
    timeout = 5
    start_time = time.time()
    up = False
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("127.0.0.1", int(port)), timeout=1):
                up = True
                break
        except Exception:
            time.sleep(0.1)

    if not up:
        proc.terminate()
        raise RuntimeError("Failed to start dev server on port " + port)

    yield f"http://127.0.0.1:{port}"

    proc.terminate()
    proc.wait()

def test_getting_started_copy_buttons(dev_server, page: Page, context):
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # Load the getting-started page
    page.goto(f"{dev_server}/docs/getting-started.html")

    # 1. Test Command Card copy button
    cmd_button = page.locator(".command-card button[data-copy]")
    expect(cmd_button).to_be_visible()
    expect(cmd_button).to_have_attribute("aria-label", "Copy commands to clipboard")
    expect(cmd_button).to_have_text(re.compile(r"Copy"))

    # Click the command card copy button
    cmd_button.click()

    # Expect temporary success feedback (either Copied or Copy failed)
    text = cmd_button.text_content().strip()
    assert text in ("Copied", "Copy failed")

    if text == "Copied":
        expect(cmd_button).to_have_class(re.compile(r"is-valid"))
        expect(cmd_button).to_have_attribute("aria-label", "Copied to clipboard")
    else:
        expect(cmd_button).to_have_class(re.compile(r"is-invalid"))
        expect(cmd_button).to_have_attribute("aria-label", "Copy failed")

    # Wait for recovery timeout (1400ms + buffer)
    page.wait_for_timeout(1600)

    # Verify restored state
    expect(cmd_button).to_have_text(re.compile(r"Copy"))
    expect(cmd_button).not_to_have_class(re.compile(r"is-valid"))
    expect(cmd_button).not_to_have_class(re.compile(r"is-invalid"))
    expect(cmd_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # 2. Test Code Card copy button
    code_button = page.locator(".code-card button[data-copy]")
    expect(code_button).to_be_visible()
    expect(code_button).to_have_attribute("aria-label", "Copy code to clipboard")
    expect(code_button).to_have_text(re.compile(r"Copy"))

    # Click the code card copy button
    code_button.click()

    text_code = code_button.text_content().strip()
    assert text_code in ("Copied", "Copy failed")

    if text_code == "Copied":
        expect(code_button).to_have_class(re.compile(r"is-valid"))
        expect(code_button).to_have_attribute("aria-label", "Copied to clipboard")
    else:
        expect(code_button).to_have_class(re.compile(r"is-invalid"))
        expect(code_button).to_have_attribute("aria-label", "Copy failed")

    # Wait for recovery timeout (1400ms + buffer)
    page.wait_for_timeout(1600)

    # Verify restored state
    expect(code_button).to_have_text(re.compile(r"Copy"))
    expect(code_button).not_to_have_class(re.compile(r"is-valid"))
    expect(code_button).not_to_have_class(re.compile(r"is-invalid"))
    expect(code_button).to_have_attribute("aria-label", "Copy code to clipboard")
