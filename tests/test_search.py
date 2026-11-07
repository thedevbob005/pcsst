from pathlib import Path


def test_search_input_escape_key_handler() -> None:
    app_js_path = Path(__file__).resolve().parent.parent / "docs" / "app.js"
    content = app_js_path.read_text(encoding="utf-8")

    assert "async function setupSearch()" in content
    assert 'event.key === "Escape"' in content
    assert 'searchInput.addEventListener("keydown"' in content
    assert "searchInput.blur()" in content
    assert 'renderSearchResults(entries, "")' in content
