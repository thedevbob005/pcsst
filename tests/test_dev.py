import sys
from pathlib import Path
from unittest.mock import patch

# Add scripts directory to sys.path to allow importing dev
sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))

import dev

def test_rewrite_root_slash():
    """Test that path '/' is rewritten to '/docs/index.html'."""
    with patch("dev.SimpleHTTPRequestHandler.__init__", return_value=None):
        handler = dev.PCSSTHandler()
        handler.path = "/"
        handler._rewrite_root()
        assert handler.path == "/docs/index.html"

def test_rewrite_root_empty():
    """Test that empty path is rewritten to '/docs/index.html'."""
    with patch("dev.SimpleHTTPRequestHandler.__init__", return_value=None):
        handler = dev.PCSSTHandler()
        handler.path = ""
        handler._rewrite_root()
        assert handler.path == "/docs/index.html"

def test_rewrite_root_other():
    """Test that other paths are not rewritten."""
    with patch("dev.SimpleHTTPRequestHandler.__init__", return_value=None):
        handler = dev.PCSSTHandler()
        handler.path = "/src/pcsst.css"
        handler._rewrite_root()
        assert handler.path == "/src/pcsst.css"

def test_do_get_calls_rewrite():
    """Test that do_GET calls _rewrite_root and super().do_GET()."""
    with patch("dev.SimpleHTTPRequestHandler.__init__", return_value=None):
        with patch("dev.SimpleHTTPRequestHandler.do_GET", return_value=None) as mock_super_get:
            handler = dev.PCSSTHandler()
            handler.path = "/"
            handler.do_GET()
            assert handler.path == "/docs/index.html"
            mock_super_get.assert_called_once()

def test_do_head_calls_rewrite():
    """Test that do_HEAD calls _rewrite_root and super().do_HEAD()."""
    with patch("dev.SimpleHTTPRequestHandler.__init__", return_value=None):
        with patch("dev.SimpleHTTPRequestHandler.do_HEAD", return_value=None) as mock_super_head:
            handler = dev.PCSSTHandler()
            handler.path = "/"
            handler.do_HEAD()
            assert handler.path == "/docs/index.html"
            mock_super_head.assert_called_once()
