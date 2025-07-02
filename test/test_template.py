import pathlib
from datetime import datetime
from subprocess import run

import pytest


@pytest.mark.parametrize("terraform_provider", ["hashicorp/aws", "hashicorp/azurerm"])
@pytest.mark.parametrize(
    "terraform_module_type", ["primitive", "collection", "reference"]
)
def test_template_renders(isolated_copy, terraform_provider, terraform_module_type):
    data = {
        "terraform_provider": terraform_provider,
        "terraform_module_type": terraform_module_type,
    }
    destination: pathlib.Path = isolated_copy(data=data, skip_tasks=True)

    assert destination.exists()
    assert destination.is_dir()

    # Check that the template rendered files
    assert destination.joinpath("README.md").exists(), "README.md was not rendered"
    assert destination.joinpath("LICENSE").exists(), "LICENSE was not rendered"
    assert destination.joinpath("NOTICE").exists(), "NOTICE was not rendered"

    # Check the year was properly inserted into the NOTICE file
    notice_contents = destination.joinpath("NOTICE").read_text()
    assert (
        str(datetime.now().year) in notice_contents
    ), "Current year not found in NOTICE file"
    assert 0, destination


def test_template_tasks(isolated_copy):
    data = {
        "terraform_provider": "hashicorp/aws",
        "terraform_module_type": "primitive",
    }
    destination: pathlib.Path = isolated_copy(data=data, skip_tasks=True)
    assert destination.exists()
    assert destination.is_dir()

    # Check that the template rendered files
    assert destination.joinpath("README.md").exists(), "README.md was not rendered"
    assert destination.joinpath("LICENSE").exists(), "LICENSE was not rendered"
    assert destination.joinpath("NOTICE").exists(), "NOTICE was not rendered"

    # Confirm terraform-docs was run against the README files
    readme_contents = destination.joinpath("README.md").read_text()
    example_readme_contents = destination.joinpath(
        "examples/minimal/README.md"
    ).read_text()
    tf_docs_marker = "<!-- BEGIN_TF_DOCS -->\n## Requirements"
    assert tf_docs_marker in readme_contents, ""
    assert tf_docs_marker in example_readme_contents

    # Confirm git init was run
    git_dir = destination.joinpath(".git")
    assert git_dir.exists(), ".git directory was not created"

    # Confirm go mod tidy was run
    go_sum_file = destination.joinpath("go.sum")
    assert go_sum_file.exists(), "go.sum file was not created"

    # Confirm make configure was run
    dot_repo_path = destination.joinpath(".repo")
    components_path = destination.joinpath("components")
    assert (
        dot_repo_path.exists() and dot_repo_path.is_dir()
    ), ".repo directory was not created"
    assert (
        components_path.exists() and components_path.is_dir()
    ), "components directory was not created"


@pytest.mark.requires_credentials
@pytest.mark.aws
@pytest.mark.parametrize("terraform_module_type", ["primitive"])
def test_rendered_repository_can_make_check_aws(isolated_copy, terraform_module_type):
    data = {
        "terraform_provider": "hashicorp/aws",
        "terraform_module_type": terraform_module_type,
    }
    destination: pathlib.Path = isolated_copy(data=data)

    assert destination.exists()
    assert destination.is_dir()

    result = run("make check", shell=True, cwd=destination, capture_output=True)
    assert (
        result.returncode == 0
    ), f"Make check failed in the rendered repository ({destination})"


@pytest.mark.requires_credentials
@pytest.mark.azure
@pytest.mark.parametrize("terraform_module_type", ["primitive"])
def test_rendered_repository_can_make_check_azurerm(
    isolated_copy, terraform_module_type
):
    data = {
        "terraform_provider": "hashicorp/azurerm",
        "terraform_module_type": terraform_module_type,
    }
    destination: pathlib.Path = isolated_copy(data=data)

    assert destination.exists()
    assert destination.is_dir()

    result = run("make check", shell=True, cwd=destination, capture_output=True)
    assert (
        result.returncode == 0
    ), f"Make check failed in the rendered repository ({destination})"
