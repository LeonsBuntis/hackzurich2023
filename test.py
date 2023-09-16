import asyncio

# Shared state
should_stop = False

async def alwaysRun():
    global should_stop
    while not should_stop:
        print("This will run forever until interrupted.")
        await asyncio.sleep(1)  # This allows other tasks to run

async def checkIfSomethingHappened():
    global should_stop
    await asyncio.sleep(5)  # Wait for 5 seconds
    print("Something happened! Stopping alwaysRun.")
    should_stop = True

loop = asyncio.get_event_loop()
task1 = asyncio.ensure_future(alwaysRun())
task2 = asyncio.ensure_future(checkIfSomethingHappened())

loop.run_until_complete(asyncio.gather(task1, task2))
