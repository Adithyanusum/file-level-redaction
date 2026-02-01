import pathlib
import pytest


@pytest.fixture(scope="session")
def fixtures_dir():
    """Path to tests fixtures directory."""
    return pathlib.Path(__file__).parent / "fixtures"
