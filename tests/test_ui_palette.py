import subprocess
import time
import socket
import sys
import re
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="module")
def dev_server():
    port = 4173
    proc = subprocess.Popen(
        [sys.executable, "scripts/dev.py"],
        env={"PORT": str(port), **subprocess.os.environ},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    start_time = time.time()
    up = False
    while time.time() - start_time < 5:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                up = True
                break
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(0.1)

    if not up:
        proc.terminate()
        raise RuntimeError("Development server did not start in time")

    yield f"http://127.0.0.1:{port}"

    proc.terminate()
    proc.wait()

def test_copy_buttons_behavior(dev_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = context.new_page()

        # 1. Test Overview page's command card copy button
        page.goto(f"{dev_server}/docs/index.html")

        btn = page.locator(".command-card button[data-copy]")
        expect(btn).to_be_visible()
        expect(btn).to_have_attribute("aria-label", "Copy commands to clipboard")

        btn.click()

        expect(btn).to_have_text(re.compile(r"Copied"))
        expect(btn).to_have_class(re.compile(r"is-valid"))
        expect(btn).to_have_attribute("aria-label", "Copied to clipboard")

        clipboard_text = page.evaluate("navigator.clipboard.readText()")
        assert "python3 scripts/build.py" in clipboard_text

        page.wait_for_timeout(1500)
        expect(btn).to_have_text("Copy")
        expect(btn).not_to_have_class(re.compile(r"is-valid"))
        expect(btn).to_have_attribute("aria-label", "Copy commands to clipboard")

        # 2. Test standard code-card copy button in getting started guide
        page.goto(f"{dev_server}/docs/getting-started.html")

        code_btn = page.locator(".code-card button[data-copy]").first
        expect(code_btn).to_be_visible()
        expect(code_btn).to_have_attribute("aria-label", "Copy code to clipboard")

        code_btn.click()
        expect(code_btn).to_have_text(re.compile(r"Copied"))
        expect(code_btn).to_have_class(re.compile(r"is-valid"))
        expect(code_btn).to_have_attribute("aria-label", "Copied to clipboard")

        browser.close()
