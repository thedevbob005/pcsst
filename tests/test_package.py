import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add scripts directory to sys.path
scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(scripts_dir))

import package

def test_create_package(tmp_path, monkeypatch):
    # Mock ROOT_DIR to use a temporary directory
    mock_root = tmp_path / "repo"
    mock_root.mkdir()
    monkeypatch.setattr(package, "ROOT_DIR", mock_root)

    # Create a fake package.json
    version = "0.3.0"
    package_json = mock_root / "package.json"
    package_json.write_text(json.dumps({"version": version}), encoding="utf-8")

    # Mock RELEASES_DIR
    mock_releases_dir = mock_root / "releases"
    monkeypatch.setattr(package, "RELEASES_DIR", mock_releases_dir)

    # Mock dependencies
    mock_export_site = MagicMock()
    mock_verify_python = MagicMock()
    mock_verify_docs = MagicMock()

    monkeypatch.setattr(package, "export_site", mock_export_site)
    monkeypatch.setattr(package, "verify_python", mock_verify_python)
    monkeypatch.setattr(package, "verify_docs", mock_verify_docs)

    with patch("tarfile.open") as mock_tar_open:
        mock_tar = MagicMock()
        mock_tar_open.return_value.__enter__.return_value = mock_tar

        archive_path = package.create_package()

        # Verify dependencies were called
        mock_export_site.assert_called_once()
        mock_verify_python.assert_called_once()
        mock_verify_docs.assert_called_once()

        # Verify directory creation
        assert mock_releases_dir.exists()

        # Verify archive path
        expected_archive_path = mock_releases_dir / f"pcsst-{version}.tgz"
        assert archive_path == expected_archive_path

        # Verify tarfile was opened correctly
        mock_tar_open.assert_called_once_with(expected_archive_path, "w:gz")

        # Verify files added to archive
        # We use a hardcoded list of expected files to ensure the test catches changes to PACKAGE_FILES
        expected_files = ["dist", "src", "docs", "README.md", "LICENSE", "package.json"]
        assert mock_tar.add.call_count == len(expected_files)
        for relative_name in expected_files:
            source = mock_root / relative_name
            arcname = f"pcsst-{version}/{relative_name}"
            mock_tar.add.assert_any_call(source, arcname=arcname)
