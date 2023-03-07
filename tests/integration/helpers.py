import random
import time
from pathlib import Path
from string import ascii_lowercase
from typing import Callable, Optional

BASE_URL = "https://api.linode.com/v4/"

COMMAND_JSON_OUTPUT = ["--suppress-warnings", "--no-defaults", "--json"]


def get_random_text(length: int = 10):
    return "".join(random.choice(ascii_lowercase) for i in range(length))


def create_file_random_text(
    name_generator: Callable,
    dir_path: Optional[Path] = None,
    filename: Optional[str] = None,
):
    if not dir_path:
        dir_path = Path(__file__).parent
    if not filename:
        filename = f"{name_generator('test-file')}.txt"
    content = "Linode CLI integration test\n" f"{get_random_text(100)}\n"
    file_path = dir_path / filename
    with open(file_path, "w") as f:
        f.write(content + "\n")
    return file_path.resolve()


def wait_for_condition(interval: int, timeout: int, condition: Callable):
    start_time = time.time()
    while True:
        if condition():
            break

        if time.time() - start_time > timeout:
            raise TimeoutError("SSH timeout expired")

        # Evil
        time.sleep(interval)
