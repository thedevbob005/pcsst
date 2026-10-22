from pathlib import Path

def test_app_js_copy_buttons():
    app_js_path = Path(__file__).parent.parent / "docs" / "app.js"
    content = app_js_path.read_text()

    assert "closest(\".code-card, .command-card\")" in content
    assert "button.setAttribute(\"aria-label\", \"Copied to clipboard\")" in content
    assert "button.classList.add(\"is-valid\")" in content
    assert "block.innerText.trim()" in content

def test_getting_started_command_card_copy_button():
    html_path = Path(__file__).parent.parent / "docs" / "getting-started.html"
    content = html_path.read_text()

    assert "aria-label=\"Copy commands to clipboard\"" in content
    assert "data-copy" in content
    assert "command-card__bar" in content
