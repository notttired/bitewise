import asyncio
from typing import List, Callable, Awaitable

async def run_async_tasks(inputs: list, worker_fn, concurrency: int = 100):
    semaphore = asyncio.Semaphore(concurrency)

    async def safe_worker(item):
        async with semaphore:
            out = None
            try:
                out = await asyncio.to_thread(worker_fn, item)
            except Exception as e:
                print(f"Error: {e}")
            return out  

    tasks = [safe_worker(i) for i in inputs]
    results = await asyncio.gather(*tasks)
    filtered = list(filter(lambda x: x, results))
    return filtered