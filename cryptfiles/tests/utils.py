from typing import Union
from pathlib import Path
from random import randint


def create_a_random_test_file(directory:Union[str,Path], ext:str) -> Path:
    while True:
        file_path = Path(f"{directory}/test{randint(1,10000)}.{ext}")
        if not file_path.exists():
            break
    file_path.touch()
    return file_path
