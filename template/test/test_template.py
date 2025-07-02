import pathlib
from contextlib import ExitStack as does_not_raise

import pytest
from copier.errors import InvalidTypeError


@pytest.mark.parametrize(
    "data, expected",
    [
        ({}, pytest.raises(InteractiveSessionError)),
        # Customize template invocation by passing specific data
        (
            {
                "answer_one": "value_one",
                "answer_two": "value_two",
            },
            does_not_raise(),
        ),
    ],
)
class TestCopierInputsRendered:
    def test_copier_render(self, isolated_copy, data, expected):
        """Test that the copier can render the template without errors."""
        with expected:
            # Checks to validate that the inputs are rendered correctly
            # need to be added here.
            assert False, "Tests have not been implemented yet!"

            # The following will give you the path to which the template was rendered:
            # destination: pathlib.Path = isolated_copy(data=data)
