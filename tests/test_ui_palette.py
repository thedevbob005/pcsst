import pytest
import re
import subprocess
import time
from playwright.sync_api import expect

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "permissions": ["clipboard-read", "clipboard-write"],
    }

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    # Start the development server
    process = subprocess.Popen(
        ["python3", "scripts/dev.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Give it a moment to start
    time.sleep(2)
    yield
    # Terminate the server
    process.terminate()

def test_copy_button_feedback(page):
    # Navigate to the getting-started page (contains both code-card and command-card)
    page.goto("http://127.0.0.1:4173/docs/getting-started.html")

    # Test code-card copy button
    code_card_btn = page.locator(".code-card [data-copy]").first
    original_label = code_card_btn.get_attribute("aria-label") or code_card_btn.inner_text()

    # Click and check feedback
    code_card_btn.click()
    expect(code_card_btn).to_have_text(re.compile(r"Copied"))
    expect(code_card_btn).to_have_class(re.compile(r"is-valid"))

    # Wait for restoration
    page.wait_for_timeout(1600)
    expect(code_card_btn).not_to_have_text(re.compile(r"Copied"))
    expect(code_card_btn).not_to_have_class(re.compile(r"is-valid"))

    # Test command-card copy button
    command_card_btn = page.locator(".command-card [data-copy]").first

    # Click and check feedback
    command_card_btn.click()
    expect(command_card_btn).to_have_text(re.compile(r"Copied"))
    expect(command_card_btn).to_have_class(re.compile(r"is-valid"))
    expect(command_card_btn).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for restoration
    page.wait_for_timeout(1600)
    expect(command_card_btn).to_have_text(re.compile(r"Copy"))
    expect(command_card_btn).to_have_attribute("aria-label", "Copy commands to clipboard")
    expect(command_card_btn).not_to_have_class(re.compile(r"is-valid"))

def test_rapid_clicks_handling(page):
    page.goto("http://127.0.0.1:4173/docs/getting-started.html")
    btn = page.locator(".command-card [data-copy]").first

    # Click multiple times rapidly
    for _ in range(5):
        btn.click()
        page.wait_for_timeout(100)

    expect(btn).to_have_text(re.compile(r"Copied"))

    # Wait and ensure it restores correctly once
    page.wait_for_timeout(1600)
    expect(btn).to_have_text(re.compile(r"Copy"))
    expect(btn).not_to_have_class(re.compile(r"is-valid"))
