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
        # events being watched
        self.awaited_events = {}
        # handlers (how to read event)
        self.handlers = {}

        ## Async IO
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
    
    def wait_for_events_before_step(self, events, step, step_args):
        """
            Define the relation between event and setps
            What is the list of event expected before triggering a step?
        """

        print(f"{step} is waiting for events: {events} to be triggered")

        if step not in self.waiting_for:
            self.waiting_for[step] = events

        for e in events:

            if e not in self.awaited_events: 
                self.awaited_events[e] = {}

            self.awaited_events[e][step] = step_args

    def transition(self, event, future_step):
        """
            Update the waiting_for dict
            Return True if the future_step don't need to wait anymore return True
            Return False otherwise
        """

        print(f"{future_step} was waiting for {event} to be triggered")

        # Event has occurred remove from list
        self.waiting_for[future_step].remove(event)

        # Transition is validated if we don't need to wait for anything for that step
        if len(self.waiting_for[future_step]) == 0:
            del self.waiting_for[future_step]
            return True

        return False

    def step(self, event, expected_state="ok"):
        """
        Manage the execution of the state machine
            1. validate Transition for impacted dependencies
            2. if Transition => start process
            3. watch new process
        """

        # is the status what we expect? (stopped//running)
        if event["state"] == expected_state:
            # do we have a future_step waiting for that event?
            if event["name"] in self.awaited_events:
                # Which future_step are candidate to be triggered?
                waiting_for_that_event = self.awaited_events[event["name"]]

                for future_step in waiting_for_that_event:
                    # Validate Transition condition
                    if self.transition(event["name"], future_step):
                        self.watch(future_step, **waiting_for_that_event[future_step])

                del self.awaited_events[event["name"]]
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
                print("event ", event)

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