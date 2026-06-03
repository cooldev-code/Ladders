import pytest

from app.config import FEEDS_DIR, PROJECT_ROOT


@pytest.fixture
def feeds_dir():
    return FEEDS_DIR


@pytest.fixture
def project_root():
    return PROJECT_ROOT
