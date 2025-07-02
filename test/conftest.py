import pathlib
from random import choices
from string import ascii_letters, digits
from typing import Callable, Generator

import pytest
from copier import run_copy
from ruamel.yaml import YAML


@pytest.fixture(scope="session")
def copier_config_all():
    """Fixture to retrieve the copier configuration as a dictionary."""
    copier_config_path = pathlib.Path(__file__).parent.parent.joinpath("copier.yml")
    yaml = YAML(typ="safe")
    with open(copier_config_path, "r") as file:
        config = yaml.load(file)
    yield config


@pytest.fixture(scope="session")
def copier_config_meta(copier_config_all):
    yield {k: v for k, v in copier_config_all.items() if k.startswith("_")}


@pytest.fixture(scope="session")
def copier_config(copier_config_all):
    yield {k: v for k, v in copier_config_all.items() if not k.startswith("_")}


@pytest.fixture(scope="session")
def copier_answers() -> Generator[Callable[[pathlib.Path], dict[str]], None, None]:
    def _copier_answers(path: pathlib.Path) -> dict[str]:
        """Return a dictionary of answers for copier from a given path."""
        copier_answers_path = path.joinpath(".copier-answers.yml")
        yaml = YAML(typ="safe")
        with open(copier_answers_path, "r") as file:
            answers = yaml.load(file)
        return answers

    yield _copier_answers


def random_directory_name(length: int = 10) -> str:
    """Generate a random directory name of a given length."""
    return "".join(choices(ascii_letters + digits, k=length))


@pytest.fixture(scope="function")
def isolated_copy(tmpdir) -> Generator[Callable[[dict[str]], pathlib.Path], None, None]:
    src_path = pathlib.Path(__file__).parent.parent

    def _isolated_copy(
        data: dict[str] = None, skip_tasks: bool = False
    ) -> pathlib.Path:
        """Run copier in an isolated output folder that will be cleaned up after the run."""
        dst_path = tmpdir.mkdir(random_directory_name())

        run_copy(
            src_path=str(src_path),
            dst_path=str(dst_path),
            data=data or {},
            defaults=True,
            unsafe=True,
            skip_tasks=skip_tasks,
        )
        return pathlib.Path(dst_path)

    yield _isolated_copy
