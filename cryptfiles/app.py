import os
import argparse
from typing import List, Union, Optional

from pathlib import Path
from cryptography.fernet import Fernet

class Crypter:
    
    allowed_extensions = (".jpg",".txt")

    def __init__(self, mode:str, target:Union[str,Path], key_scan:bool, key:Optional[str]=None) -> None:
        self.mode = mode
        self.target= Path(target)
        self.key_scan = key_scan
        self.key = key

    def run(self):
        print(self.locate_files())

    def locate_files(self) -> List[Optional[Path]]:
        file_paths = []

        if self.target.is_file() and self.is_ext_allowed(self.target):
            return [self.target]

        # If target is a directory
        for dirpath, dirnames, filenames in os.walk(self.target):
            for filename in filenames:
                if self.is_ext_allowed(filename):
                    file_path = Path(f"{dirpath}/{filename}")
                    file_paths.append(file_path)
        return file_paths

    def is_ext_allowed(self, path:Union[str,Path]) -> bool:
        file_extension = os.path.splitext(Path(path))[1]
        return file_extension.lower() in self.allowed_extensions


    def execute_selected_mode(self, files:List[Path]) -> None:
        if files:
            if self.mode == 'encrypt':
                self.encrypt_files(files)
            else:
                self.decrypt_files(files) 
        

    def encrypt_files(self, file_paths:List[Path]) -> None:
        pass

    def decrypt_files(self, file_paths:List[Path]) -> None:
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
        help="Specifies the key code to be used."
    )
    # Define keyscan
    key_group.add_argument(
        "-ks",
        "--keyscan",
        action="store_true",
        dest="key_scan",
        help="Defines whether cryptofiles should look up the key file."
    )

    # Define directory/path to execute.
    parser.add_argument(
        "-t",
        "--target",
        action="store",
        metavar="DIR|PATH",
        required=True,
        type=str,
        help="Directory or Path to encrypt/decrypt."
    )

    args = parser.parse_args()
    
    crypter = Crypter(
        mode = "encrypt" if args.encrypt else "decrypt",
        target= args.directory,
        key_scan= args.key_scan,
        key= args.key
    )
    crypter.run()