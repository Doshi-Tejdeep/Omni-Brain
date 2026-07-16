"""Basic checks that keep the initial project structure healthy."""

from pathlib import Path


def test_project_has_readme() -> None:
    """Every checkout should include the project overview."""
    assert Path("README.md").is_file()
