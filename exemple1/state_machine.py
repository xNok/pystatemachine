import os
import asyncio

def main():
    create_loop(manifest)

def create_loop(manifest):

    ## State Machine Execute Actions
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        task_loop(manifest)
    )
    loop.close()

async def task(context):
    pass

async def task_loop(manifest):
    added_tasks = []

    print('Async task creation: adding tasks')

    for context in manifest:

        t = asyncio.create_task(
            task(context)
        )

        added_tasks.append(t)

    print('Async task creation: done adding tasks')

    running_tasks = added_tasks[::]

    # wait until we see that all tasks have completed
    while running_tasks:
        running_tasks = [x for x in running_tasks if not x.done()]
        await asyncio.sleep(0)

    print('Async task execution: done running tasks')


if __name__ == '__main__':
    main()