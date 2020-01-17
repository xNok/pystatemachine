import pytest
import asyncio
import random

from .event_driven_state_machine import event_driven_state_machine

class Test:

    def test_run_nodeps(self):

        sm = event_driven_state_machine()

        ## Adding initial tasks
        delays = [x for x in range(5)]

        # shuffle to simulate unknown run times
        random.shuffle(delays)

        for n in delays:
            sm.watch(n, time=n/10)

        results = sm.run_until_complete()

        assert sm.report == [
            {"name": 0, "state": 'ok', 'duration': 0},
            {"name": 1, "state": 'ok', 'duration': 1/10},
            {"name": 2, "state": 'ok', 'duration': 2/10},
            {"name": 3, "state": 'ok', 'duration': 3/10},
            {"name": 4, "state": 'ok', 'duration': 4/10}
        ]

    def test_run_withdeps(self):

        sm = event_driven_state_machine()

        ## Adding initial tasks
        delays = [x for x in range(5)]

        # shuffle to simulate unknown run times
        random.shuffle(delays)

        sm.wait_for_events_before_step([1], "child 1", {"time": 1/10})

        for n in delays:
            sm.watch(n, time=n/10)

        results = sm.run_until_complete()

        assert sm.report == [
            {"name": 0, "state": 'ok', 'duration': 0},
            {"name": 1, "state": 'ok', 'duration': 1/10},
            {'name': 'child 1', 'state': 'ok', 'duration': 1/10},
            {"name": 2, "state": 'ok', 'duration': 2/10},
            {"name": 3, "state": 'ok', 'duration': 3/10},
            {"name": 4, "state": 'ok', 'duration': 4/10}
        ]

    def test_run_withcomplexdeps(self):

        sm = event_driven_state_machine()

        ## Adding initial tasks
        delays = [x for x in range(5)]

        # shuffle to simulate unknown run times
        random.shuffle(delays)

        sm.wait_for_events_before_step([1], "child 1", {"time": 1/10})
        sm.wait_for_events_before_step([2,3], "child 2/3", {"time": 1/10})
        sm.wait_for_events_before_step(["child 1","child 2/3"], "child 1/2/3", {"time": 1/10})

        for n in delays:
            sm.watch(n, time=n/10)

        results = sm.run_until_complete()

        # child 1     -> 1/10 + 1/10
        # child 2/3   -> 5/10 + 1/10
        # child 1/2/3 -> 6/10 + 1/10

        assert sm.report == [
            {"name": 0, "state": 'ok', 'duration': 0},
            {"name": 1, "state": 'ok', 'duration': 1/10},
            {'name': 'child 1', 'state': 'ok', 'duration': 1/10},
            {"name": 2, "state": 'ok', 'duration': 2/10},
            {"name": 3, "state": 'ok', 'duration': 3/10},
            {'name': 'child 2/3', 'state': 'ok', 'duration': 0.1},
            {"name": 4, "state": 'ok', 'duration': 4/10},
            {'name': 'child 1/2/3', 'state': 'ok', 'duration': 0.1}
        ]