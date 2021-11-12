from pathlib import Path
from shutil import rmtree

import pytest

@pytest.fixture
def testfiles_path():
    return Path("./testfiles")

@pytest.fixture(scope="function", autouse=True)
def create_testfiles_folder(testfiles_path):
    if testfiles_path.exists():
        # Remove the folder AND the mainly child files
        rmtree(testfiles_path)
    # Create a clean folder
    testfiles_path.mkdir()
    yield testfiles_path
    # Remove path when the fixture is destroyed
    rmtree(testfiles_path)