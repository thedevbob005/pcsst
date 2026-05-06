import sys
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts directory to sys.path to allow importing modules from there
scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(scripts_dir))

import export_site


@pytest.fixture
def mock_repo_structure(tmp_path):
    """Sets up a mock repository structure in a temporary directory."""
    root_dir = tmp_path / "repo"
    root_dir.mkdir()

    # Create source files/dirs
    (root_dir / "index.html").write_text("index content", encoding="utf-8")

    docs_dir = root_dir / "docs"
    docs_dir.mkdir()
    (docs_dir / "doc.html").write_text("doc content", encoding="utf-8")

    dist_dir = root_dir / "dist"
    dist_dir.mkdir()
    (dist_dir / "pcsst.css").write_text("css content", encoding="utf-8")

    return root_dir


def test_export_site_creates_directory_and_copies_files(mock_repo_structure):
    root_dir = mock_repo_structure
    site_dir = root_dir / "site"

    with patch("export_site.ROOT_DIR", root_dir), \
         patch("export_site.SITE_DIR", site_dir), \
         patch("export_site.build") as mock_build:

        exported_dir = export_site.export_site()

        # Verify build was called
        mock_build.assert_called_once()

        # Verify site directory exists
        assert exported_dir == site_dir
        assert site_dir.exists()
        assert site_dir.is_dir()

        # Verify files/dirs were copied
        assert (site_dir / "index.html").read_text(encoding="utf-8") == "index content"
        assert (site_dir / "docs" / "doc.html").read_text(encoding="utf-8") == "doc content"
        assert (site_dir / "dist" / "pcsst.css").read_text(encoding="utf-8") == "css content"

        # Verify 404.html was created
        assert (site_dir / "404.html").exists()
        assert "Redirecting to the PCSST docs" in (site_dir / "404.html").read_text(encoding="utf-8")


def test_export_site_cleans_existing_directory(mock_repo_structure):
    root_dir = mock_repo_structure
    site_dir = root_dir / "site"
    site_dir.mkdir(parents=True)
    (site_dir / "old_file.txt").write_text("old content", encoding="utf-8")

    with patch("export_site.ROOT_DIR", root_dir), \
         patch("export_site.SITE_DIR", site_dir), \
         patch("export_site.build"):

        export_site.export_site()

        # Verify old file is gone
        assert not (site_dir / "old_file.txt").exists()
        # Verify new files are present
        assert (site_dir / "index.html").exists()
