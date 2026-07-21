import re
import pytest
from playwright.sync_api import expect


def test_getting_started_copy_buttons(page):
    # Navigate to the getting started page on our running dev server
    page.goto("http://localhost:4173/docs/getting-started.html")

    # Give browser context the proper clipboard permissions if supported
    # In Playwright python, we can grant permissions on context level
    context = page.context
    context.grant_permissions(["clipboard-read", "clipboard-write"])

    # 1. Verify Command Card Copy Button
    command_button = page.locator('.command-card [data-copy]')
    expect(command_button).to_be_visible()
    expect(command_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # Click and verify feedback state
    command_button.click()
    expect(command_button).to_have_text(re.compile(r"Copied"))
    expect(command_button).to_have_class(re.compile(r"is-valid"))
    expect(command_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait for state restoration (1400ms timeout) and verify restored state
    page.wait_for_timeout(1600)
    expect(command_button).to_have_text("Copy")
    expect(command_button).not_to_have_class(re.compile(r"is-valid"))
    expect(command_button).to_have_attribute("aria-label", "Copy commands to clipboard")

    # 2. Verify Standard Code Card Copy Button
    code_button = page.locator('.code-card [data-copy]')
    expect(code_button).to_be_visible()
    expect(code_button).to_have_attribute("aria-label", "Copy code to clipboard")

    # Click and verify feedback state
    code_button.click()
    expect(code_button).to_have_text(re.compile(r"Copied"))
    expect(code_button).to_have_class(re.compile(r"is-valid"))
    expect(code_button).to_have_attribute("aria-label", "Copied to clipboard")

    # Wait and verify restored state
    page.wait_for_timeout(1600)
    expect(code_button).to_have_text("Copy")
    expect(code_button).not_to_have_class(re.compile(r"is-valid"))
    expect(code_button).to_have_attribute("aria-label", "Copy code to clipboard")
