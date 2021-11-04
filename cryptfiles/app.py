import os
import argparse
from typing import List, Union, Optional

from pathlib import Path, PosixPath, WindowsPath
from cryptography.fernet import Fernet

class Crypter:

    encrypt_ext = (".jpg",)

    def __init__(self, mode:str, directory:str, key_scan:bool, key:Optional[str]=None) -> None:
        self.mode = mode
        self.directory= Path(directory)
        self.key_scan = key_scan
        self.key = key

    def run(self):
        print(self.locate_files())

    def locate_files(self) -> List[Optional[Union[PosixPath, WindowsPath]]]:
        file_paths = []
        for dirpath, dirnames, filenames in os.walk("."): # TODO: pass folder by args
            for filename in filenames:
                _, file_ext = os.path.splitext(filename)
                if file_ext.lower() in self.encrypt_ext:
                    file_path = Path(f"{dirpath}/{filename}")
                    file_paths.append(file_path)
        return file_paths

    def execute_selected_mode(self, files) -> None:
        if files:
            if self.mode == 'encrypt':
                self.encrypt_files(files)
            else:
                self.decrypt_files(files) 
        

    def encrypt_files(self, file_paths:List[Union[PosixPath, WindowsPath]]) -> None:
        pass

    def decrypt_files(self, file_paths:List[Union[PosixPath, WindowsPath]]) -> None:
        pass

    def generate_key(self):
        key = Fernet.generate_key()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("cryptfiles")

    # Define the action(encrypt/decrypt) mode
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "-e","--encrypt",action="store_true", help="Run in encryption mode."
    )
    action_group.add_argument(
        "-d","--decrypt",action="store_true", help="Run in decryption mode."
    )

    # Define key group
    key_group = parser.add_mutually_exclusive_group()
    key_group.add_argument(
        "-k",
        "-key",
        action="store",
        metavar="KEY",
        dest="key",
        help="Specifies the key to be used."
    )
    # Define keyscan
    key_group.add_argument(
        "-ks",
        "--keyscan",
        action="store_true",
        dest="key_scan",
        help="Defines whether cryptofiles should look up the key."
    )

    # Define directory to execute.
    parser.add_argument(
        "-dir",
        "--directory",
        action="store",
        default=".",
        type=str,
        help="Directory where the encrypt/decrypt starts (default: \".\")"
    )

    args = parser.parse_args()
    
    crypter = Crypter(
        mode = "encrypt" if args.encrypt else "decrypt",
        directory= args.directory,
        key_scan= args.key_scan,
        key= args.key
    )
    crypter.run()