import time
import asyncio
import aioprocessing


def func(queue, event, lock, items):
    """ Demo worker function.

    This worker function runs in its own process, and uses
    normal blocking calls to aioprocessing objects, exactly 
    the way you would use oridinary multiprocessing objects.

    """
    with lock:
        print("func set for event",  event)
        event.set()
        for item in items:
            time.sleep(3)
            queue.put(item+5)
    queue.close()


async def example(queue, event, lock):
    l = [1,2,3,4,5]
    p = aioprocessing.AioProcess(target=func, args=(queue, event, lock, l))
    p.start()
    while True:
        result = await queue.coro_get()
        if result is None:
            break
        print("Got result {}".format(result))
    await p.coro_join()

async def example2(queue, event, lock):
    print("example2 Waiting for event",  event)
    await event.coro_wait()
    print("example2 after Waiting for event",  event)
    async with lock:
        await queue.coro_put(78)
        await queue.coro_put(None) # Shut down the worker
event = aioprocessing.AioEvent()
lock = aioprocessing.AioLock()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    queue = aioprocessing.AioQueue()
    lock = aioprocessing.AioLock()
    
    tasks = [
        asyncio.ensure_future(example(queue, event, lock)), 
        asyncio.ensure_future(example2(queue, event, lock)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()