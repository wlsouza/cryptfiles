import pytest

from cryptfiles.tests.utils import create_a_test_file
from cryptfiles.app import Crypter

@pytest.fixture
def encryptmode_crypter(testfiles_path) -> Crypter:
    return Crypter(mode="encrypt",target=testfiles_path,key_scan=False)

def test_locate_files_method_must_return_a_list_with_file_paths_if_exist_files(encryptmode_crypter):
    expected = [
        create_a_test_file(encryptmode_crypter.target,"jpg"),
        create_a_test_file(encryptmode_crypter.target,"txt")
    ]
    result = encryptmode_crypter.locate_files()
    assert sorted(result) == sorted(expected)

def test_locate_files_method_must_return_a_empty_list_if_not_exist_files(encryptmode_crypter):
    result = encryptmode_crypter.locate_files()
    assert result == []

def test_locate_files_method_must_list_just_files_with_valid_extension(encryptmode_crypter):
    expected = [
        create_a_test_file(encryptmode_crypter.target,"jpg"),
        create_a_test_file(encryptmode_crypter.target,"txt")
    ]
    create_a_test_file(encryptmode_crypter.target,"test")
    result = encryptmode_crypter.locate_files()
    assert sorted(result) == sorted(expected)

