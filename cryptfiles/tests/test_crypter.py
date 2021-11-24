import pytest
from unittest import mock

from cryptfiles.tests.utils import create_a_random_test_file
from cryptfiles.app import Crypter

@pytest.fixture
def encryptmode_crypter(testfiles_path) -> Crypter:
    return Crypter(mode="encrypt",target=testfiles_path,key_scan=False)

@pytest.fixture
def decryptmode_crypter(testfiles_path) -> Crypter:
    return Crypter(mode="decrypt",target=testfiles_path,key_scan=False)

#region locate_files method
def test_locate_files_method_must_return_a_list_with_file_paths_if_exist_files(encryptmode_crypter):
    expected = [
        create_a_random_test_file(encryptmode_crypter.target,"jpg"),
        create_a_random_test_file(encryptmode_crypter.target,"txt")
    ]
    result = encryptmode_crypter.locate_files()
    assert sorted(result) == sorted(expected)

def test_locate_files_method_must_return_a_empty_list_if_not_exist_files(encryptmode_crypter):
    result = encryptmode_crypter.locate_files()
    assert result == []

def test_locate_files_method_must_list_just_files_with_valid_extension(encryptmode_crypter):
    expected = [
        create_a_random_test_file(encryptmode_crypter.target,"jpg"),
        create_a_random_test_file(encryptmode_crypter.target,"txt"),
    ]
    create_a_random_test_file(encryptmode_crypter.target,"notallowedextension")
    result = encryptmode_crypter.locate_files()
    assert sorted(result) == sorted(expected)

def test_locate_files_method_work_with_a_specific_file_instead_a_directory(testfiles_path):
    expected = [
        create_a_random_test_file(testfiles_path,"txt")
    ]
    crypter = Crypter(mode="encrypt",target=expected[0], key_scan=False)
    result = crypter.locate_files()
    assert result == expected

def test_locate_files_method_returns_empty_list_if_specific_file_does_not_exist(testfiles_path):
    crypter = Crypter(mode="encrypt",target=f"{testfiles_path}/test_non_existent_file.txt",key_scan=False)
    result = crypter.locate_files()
    assert result == []

def test_locate_files_method_returns_empty_list_if_specific_file_extension_is_not_allowed(testfiles_path):
    file_path = create_a_random_test_file(testfiles_path,"notallowedextension")
    crypter = Crypter(mode="encrypt",target=file_path, key_scan=False)
    result = crypter.locate_files()
    assert result == []
#endregion

#region is_ext_allowed method
def test_is_ext_allowed_method_returns_true_when_file_ext_is_in_allowed_extensions_list_of_crypter(encryptmode_crypter):
    ext = encryptmode_crypter.allowed_extensions[0]
    file_path = create_a_random_test_file(encryptmode_crypter.target,ext)
    result = encryptmode_crypter.is_ext_allowed(file_path)
    assert result == True

def test_is_ext_allowed_method_returns_false_when_file_ext_is_not_in_allowed_extensions_list_of_crypter(encryptmode_crypter):
    file_path = create_a_random_test_file(encryptmode_crypter.target,"notallowedextension")
    result = encryptmode_crypter.is_ext_allowed(file_path)
    assert result == False
#endregion


@mock.patch.object(Crypter, "encrypt_files")
def test_if_execute_selected_mode_method_calls_encrypt_files_method_passing_the_files_list_when_crypter_class_is_instanciated_in_encrypt_mode(encrypt_files, encryptmode_crypter):
    files = [mock.Mock(), mock.Mock()]
    encryptmode_crypter.execute_selected_mode(files)
    encrypt_files.assert_called_with(files)

@mock.patch.object(Crypter, "decrypt_files")
def test_if_execute_selected_mode_method_calls_encrypt_files_method_passing_the_files_list_when_crypter_class_is_instanciated_in_decrypt_mode(decrypt_files, decryptmode_crypter):
    files = [mock.Mock(), mock.Mock()]
    decryptmode_crypter.execute_selected_mode(files)
    decrypt_files.assert_called_with(files)
encryptmode_crypter