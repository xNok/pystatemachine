import asyncio
import random

class event_driven_state_machine(object):

    async def add_event(self, n):
        print('starting ' + str(n))
        await asyncio.sleep(n)
        print('ending ' + str(n))
        return n


    async def main(self, loop):

        added_tasks = []

        delays = [x for x in range(5)]

        # shuffle to simulate unknown run times
        random.shuffle(delays)

        for n in delays:
            print('adding ' + str(n))
            task = loop.create_task(self.add_event(n))
            added_tasks.append(task)
            await asyncio.sleep(0)

        print('done adding tasks')

        # make a list of tasks that (maybe) haven't completed
        running_tasks = added_tasks[::]

        # wait until we see that all tasks have completed
        while running_tasks:
            running_tasks = [x for x in running_tasks if not x.done()]
            await asyncio.sleep(0)

        print('done running tasks')

        # extract the results from the tasks and return them
        results = [x.result() for x in added_tasks]
        return results

sm = event_driven_state_machine()
loop = asyncio.get_event_loop()
results = loop.run_until_complete(sm.main(loop))
loop.close()
print(results)