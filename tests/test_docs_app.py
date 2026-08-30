from pathlib import Path

def test_docs_app_escape_key_search_handler():
    app_js = Path("docs/app.js").read_text(encoding="utf-8")
    assert 'event.key === "Escape"' in app_js
    assert 'searchInput.value = ""' in app_js
    assert "searchInput.blur()" in app_js
