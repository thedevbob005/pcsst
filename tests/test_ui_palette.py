import subprocess, time, pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="module", autouse=True)
def dev_server():
    p = subprocess.Popen(["python3", "scripts/dev.py"])
    time.sleep(1); yield; p.terminate()

def test_theme_switcher(page: Page):
    page.goto("http://localhost:4173/docs/index.html")
    expect(page.get_by_label("Treasure theme")).to_have_attribute("aria-pressed", "true")
    page.get_by_label("Reef theme").click()
    expect(page.get_by_label("Reef theme")).to_have_attribute("aria-pressed", "true")
