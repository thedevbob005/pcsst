import socket
import subprocess
import time
import pytest
import re
from playwright.sync_api import sync_playwright, expect

def wait_for_port(port, host="127.0.0.1", timeout=5.0):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except OSError:
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.1)

@pytest.fixture(scope="session", autouse=True)
def dev_server():
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if not wait_for_port(4173):
        process.terminate()
        raise RuntimeError("Dev server did not start.")
    yield
    process.terminate()
    process.wait()

def test_command_card_copy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = context.new_page()
        page.goto("http://localhost:4173/docs/getting-started.html")

        # Find command card copy button
        cmd_btn = page.locator('.command-card button[data-copy]')
        expect(cmd_btn).to_be_visible()
        expect(cmd_btn).to_have_attribute("aria-label", "Copy commands to clipboard")

        # Click it
        cmd_btn.click()

        # Check visual state changes
        expect(cmd_btn).to_have_text(re.compile(r"Copied"))
        expect(cmd_btn).to_have_class(re.compile(r"is-valid"))
        expect(cmd_btn).to_have_attribute("aria-label", "Copied to clipboard")

        # Verify clipboard content
        clipboard_text = page.evaluate("navigator.clipboard.readText()")
        expected_text = (
            "python3 scripts/build.py\n"
            "python3 scripts/verify.py\n"
            "python3 scripts/dev.py\n"
            "python3 scripts/export_site.py"
        )
        assert clipboard_text.strip() == expected_text.strip()

        # Wait for restoration
        page.wait_for_timeout(1500)
        expect(cmd_btn).to_have_text(re.compile(r"Copy"))
        expect(cmd_btn).to_have_attribute("aria-label", "Copy commands to clipboard")
        # Ensure is-valid is removed
        assert "is-valid" not in (cmd_btn.get_attribute("class") or "")

        browser.close()

def test_code_card_copy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = context.new_page()
        page.goto("http://localhost:4173/docs/getting-started.html")

        # Find code card copy button
        code_btn = page.locator('.code-card button[data-copy]')
        expect(code_btn).to_be_visible()
        expect(code_btn).to_have_attribute("aria-label", "Copy code to clipboard")

        # Click it
        code_btn.click()

        # Check visual state changes
        expect(code_btn).to_have_text(re.compile(r"Copied"))
        expect(code_btn).to_have_class(re.compile(r"is-valid"))
        expect(code_btn).to_have_attribute("aria-label", "Copied to clipboard")

        # Wait for restoration
        page.wait_for_timeout(1500)
        expect(code_btn).to_have_text(re.compile(r"Copy"))
        expect(code_btn).to_have_attribute("aria-label", "Copy code to clipboard")
        # Ensure is-valid is removed
        assert "is-valid" not in (code_btn.get_attribute("class") or "")

        browser.close()
