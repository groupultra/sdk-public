import time
import asyncio
import aioprocessing
async def funp_s():
    await asyncio.sleep(0.2)
async def funp():
    await asyncio.sleep(3)
def func(queue, event, lock, items, loop):
    """ Demo worker function.

    This worker function runs in its own process, and uses
    normal blocking calls to aioprocessing objects, exactly 
    the way you would use oridinary multiprocessing objects.

    """
    
    # with lock:
    print("func set for event",  event)
    # loop.run_until_complete(funp_s())
    # event.set()
    for item in items:
        # time.sleep(1)
        queue.put(item+5)
    queue.close()


async def example(queue, event, lock):
    l = [1,2,3,4,5]
    p = aioprocessing.AioProcess(target=func, args=(queue, event, lock, l, loop))
    p.start()
    while True:
        print("getting")
        result = await queue.coro_get()
        # if result is None:
        #     break
        print("Got result {}".format(result))
    # await p.coro_join()

async def example2(queue, event, lock):
    print("example2 Waiting for event",  event)
    await event.coro_wait()
    print("example2 after Waiting for event",  event)
    async with lock:
        await queue.coro_put(78)
        await queue.coro_put(None) # Shut down the worker
event = aioprocessing.AioEvent()
lock = aioprocessing.AioLock()
loop = asyncio.get_event_loop()
queue = aioprocessing.AioQueue()
lock = aioprocessing.AioLock()

async def run_example():
    asyncio.create_task(example(queue, event, lock))
    await asyncio.sleep(3)
if __name__ == "__main__":
    
    
    # tasks = [
    #     asyncio.ensure_future(example(queue, event, lock)), 
    #     # asyncio.ensure_future(example2(queue, event, lock)),
    # ]
    # loop = asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    # asyncio.create_task(example(queue, event, lock))
    # asyncio.get_event_loop().run_until_complete(example(queue, event, lock))
    
    
    loop.run_until_complete(run_example())
    # p = aioprocessing.AioProcess(target=func, args=(queue, event, lock, [1,2,3,4,5], loop))
    # p.start()
    # asyncio.create_task(example(queue, event, lock))
    print("here")
    # time.sleep(1)
    loop.run_until_complete(funp())
    # loop.run_until_complete(funp())
    # loop.run_until_complete(funp())
    # asyncio.get_event_loop().run_until_complete(funp())
    
    # asyncio.create_task(asyncio.wait(example2(queue, event, lock)))
    # print("here")
    # asyncio.create_task(asyncio.wait(example(queue, event, lock)))
    # p = aioprocessing.AioProcess(target=func, args=(queue, event, lock, [1,2,3,4,5]))
    # p.start()
    # loop.close()