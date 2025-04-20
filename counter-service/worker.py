from config import TEMPORAL_ADDRESS, TASK_QUEUE
from temporalio.client import Client
from temporalio.worker import Worker, SharedStateManager
from activity import request_payment, serve_coffee
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import asyncio

async def _run_worker():
    client = await Client.connect(TEMPORAL_ADDRESS)
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        activities=[request_payment, serve_coffee],
        activity_executor=ProcessPoolExecutor(2),
        shared_state_manager=SharedStateManager.create_from_multiprocessing(
            multiprocessing.Manager()
        ),
        max_concurrent_activities=2,
    )
    await worker.run()

def run_worker_process():
    asyncio.run(_run_worker())