from pathlib import Path


def test_nav_toggle_escape_key_handler() -> None:
    app_js_path = Path(__file__).resolve().parent.parent / "docs" / "app.js"
    content = app_js_path.read_text(encoding="utf-8")

    assert "function registerNavToggle()" in content
    assert 'event.key === "Escape"' in content
    assert 'navMenu.classList.contains("is-open")' in content
    assert 'navToggle.setAttribute("aria-expanded", "false")' in content
    assert "navToggle.focus()" in content
