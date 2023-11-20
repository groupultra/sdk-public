# # import time
# # import asyncio
# # import aioprocessing
# # async def funp_s():
# #     await asyncio.sleep(0.2)
# # async def funp():
# #     await asyncio.sleep(1)
    
# # parent_pipe, child_pipe = aioprocessing.AioPipe()
# # def func(queue, items, ):
# #     """ Demo worker function.

# #     This worker function runs in its own process, and uses
# #     normal blocking calls to aioprocessing objects, exactly 
# #     the way you would use oridinary multiprocessing objects.

# #     """
    
# #     # with lock:
    
# #     # event.set()
# #     for item in items:
# #         # time.sleep(1)
# #         asyncio.get_event_loop().run_until_complete(funp())
# #         parent_pipe.send(item)
# #         # queue.put(item+5)
# #     queue.close()


# # async def example(queue):
    
# #     while True:
# #         print("getting")
# #         # result = await queue.coro_get()
# #         result = await child_pipe.coro_recv()
# #         # if result is None:
# #         #     break
# #         print("Got result {}".format(result))
# #     # await p.coro_join()




# # async def run_example():
# #     asyncio.create_task(example(queue))
# #     # await asyncio.sleep(3)
# # if __name__ == "__main__":
# #     event = aioprocessing.AioEvent()
# #     lock = aioprocessing.AioLock()
# #     loop = asyncio.get_event_loop()
# #     print("loop", loop)
# #     queue = aioprocessing.AioQueue()
    
# #     # tasks = [
# #     #     asyncio.ensure_future(example(queue, event, lock)), 
# #     #     # asyncio.ensure_future(example2(queue, event, lock)),
# #     # ]
# #     # loop = asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
# #     # asyncio.create_task(example(queue, event, lock))
# #     # asyncio.get_event_loop().run_until_complete(example(queue, event, lock))
    
# #     l = [1,2,3,4,5]
# #     p = aioprocessing.AioProcess(target=func, args=(queue, l))
# #     p.start()
# #     loop.run_until_complete(run_example())
# #     # p = aioprocessing.AioProcess(target=func, args=(queue, event, lock, [1,2,3,4,5], loop))
# #     # p.start()
# #     # asyncio.create_task(example(queue, event, lock))
# #     print("here")
# #     # time.sleep(1)
# #     # loop.run_until_complete(funp())
# #     # loop.run_until_complete(funp())
# #     # loop.run_until_complete(funp())
# #     # asyncio.get_event_loop().run_until_complete(funp())
    
# #     # asyncio.create_task(asyncio.wait(example2(queue, event, lock)))
# #     # print("here")
# #     # asyncio.create_task(asyncio.wait(example(queue, event, lock)))
# #     # p = aioprocessing.AioProcess(target=func, args=(queue, event, lock, [1,2,3,4,5]))
# #     # p.start()
# #     # loop.close()


# import time
# import threading

# c = 0



# class T:
#     @staticmethod
#     def count_loop():
#         global c

#         while True:
#             c += 1
#             print('Count:', c)
#             time.sleep(1)
#     def threading_test(self):
#         # global c

#         t = threading.Thread(target=T.count_loop)
#         t.start()

# if __name__ == "__main__":
#     tx=T()
#     tx.threading_test()
#     time.sleep(3)
#     print('Count:', c)

import asyncio
import time
import threading
import aioprocessing

def do_it(started):
    '''Process tasks in the queue until the sentinel value is received'''
    _sentinel = 'STOP'

    def clock():
        return time.strftime("%X")

    async def process(name, total_time):
        status = f'{clock()} {name}_{total_time}:'
        print(status, 'START')
        current_time = time.time()
        end_time = current_time + total_time
        while current_time < end_time:
            print(status, 'processing...')
            await asyncio.sleep(1)
            current_time = time.time()
        print(status, 'DONE.')

    async def main():
        started.loop = asyncio.get_running_loop()
        # started.queue = task_queue = asyncio.Queue()
        started.queue = task_queue = aioprocessing.AioQueue()
        started.set()
        while True:
            item = await task_queue.get()
            if item == _sentinel:
                task_queue.task_done()
                break
            task = asyncio.create_task(process(*item))
            task.add_done_callback(lambda _: task_queue.task_done())
        await task_queue.join()

    print('event loop start')
    asyncio.run(main())
    print('event loop end')

if __name__ == '__main__':
    started = threading.Event()
    th = threading.Thread(target=do_it, args=(started,))
    th.start()
    started.wait()
    tasks, loop = started.queue, started.loop

    loop.call_soon_threadsafe(tasks.put_nowait, ('abc', 5))
    loop.call_soon_threadsafe(tasks.put_nowait, ('def', 3))
    loop.call_soon_threadsafe(tasks.put_nowait, 'STOP')