import pytest
import os
import asyncio

from unittest.mock import call, Mock, patch

from exemple1.state_machine import create_loop

@patch('exemple1.state_machine.task')
def test_create_loop(task_mock):

    ## GIVEN
    manifest = ["context1", "context2"]

    f = asyncio.Future()
    f.set_result('whatever result you want')
    task_mock.return_value = f

    ## WHEN
    create_loop(manifest)

    # THEN: calls to secret_provisonning to create task
    calls = [
        call("context1"),
        call("context2")
    ]

    assert task_mock.call_count == 2
    task_mock.assert_has_calls(calls)