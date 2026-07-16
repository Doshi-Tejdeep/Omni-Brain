from pathlib import Path


def test_project_has_readme() -> None:
    assert Path("README.md").is_file()
