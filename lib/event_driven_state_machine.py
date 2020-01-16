import asyncio
import time
import random

from .mock_event_handler import mock_random_time_handler as default_event_handler

class event_driven_state_machine(object):

    def __init__(self):

        # Active Steps
        self.event_pile = []
        # Transitions (event-driven)
        self.waiting_for = {}
        # handlers (how to read event)
        self.handlers = {}
        # Async IO event-loop
        self.loop = asyncio.new_event_loop()
        # Async IO tasks
        self.added_tasks = []
        self.report = []

    def watch(self, event, **Kargs):
        print('adding ' + str(event))
        task = self.loop.create_task(self.add_event_handler(event, **Kargs))
        self.added_tasks.append(task)

    async def add_event_handler(self, event, eventHandler=default_event_handler, **Kargs):
        """Add service to the event pile"""
        print('starting ' + str(event))
        event_result = await default_event_handler(name=event, **Kargs)
        self.event_pile.append(event_result)
        print('ending ' + str(event))
        return event_result
    
    def wait_for_before(self, passed_events, event, event_args):
        """Chain event en completion"""

        for pe in passed_events:

            if pe not in self.waiting_for: 
                self.waiting_for[pe] = {}

            self.waiting_for[pe][event] = event_args

    def update_state_machine(self, event, dep_event):
        """Make sure services that are now in the desire state are removed from waiting_for"""
        del self.waiting_for[event][dep_event]

        if len(self.waiting_for[event]) == 0:
                del self.waiting_for[event]

    def step(self, event, expected_state="ok"):
            """
            Manage the execution of the state machine
                1. validate Transition for impacted dependencies
                2. if Transition => start process
                3. watch new process
            """

            # is the status what we expect? (stopped//running)
            if event["state"] == expected_state:
                # do we have a future_event waiting for that event?
                if event["name"] in self.waiting_for:
                    # Which future_event are candidate for it?
                    waiting_for = self.waiting_for[event["name"]].copy() # we mutate waiting_for below
                    for dep_event in waiting_for:
                        # Update state machine
                        self.update_state_machine(event["name"], dep_event)

                        self.watch(dep_event, **waiting_for[dep_event])
            else: 
                # invalid state put event back to the queue
                self.event_pile.append(event)

    def readEventFromMessageQueue(self):
        """return oldest async event collect"""

        return self.event_pile.pop(0)

    async def main(self):

        # wait until we see that all tasks have completed
        while self.added_tasks or len(self.event_pile) != 0:

            if len(self.event_pile) != 0:
                event = self.readEventFromMessageQueue()
                print(event)

                self.step(event)
                self.report.append(event)

            self.added_tasks = [x for x in self.added_tasks if not x.done()]

            await asyncio.sleep(0)

        print('done running tasks')

        # extract the results from the tasks and return them
        results = [x.result() for x in self.added_tasks]
        return results

    def run_until_complete(self):

        results = self.loop.run_until_complete(self.main())
        self.loop.close()

        return results