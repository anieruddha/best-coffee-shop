import asyncio
import uvicorn
from temporalio.worker import Worker
from temporalio.client import Client
from activity import request_payment, serve_coffee
from config import TEMPORAL_ADDRESS, TASK_QUEUE, DEFAULT_WEB_APP_PORT
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
import os
from webapp import routes

async def run_worker():
    print(TEMPORAL_ADDRESS)
    client = await Client.connect(TEMPORAL_ADDRESS)
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        activities=[request_payment, serve_coffee],
    )
    await worker.run()


def configure_app():
    app = Starlette(routes=routes)
    return CORSMiddleware(
        app=app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

async def main():
    app_port = os.getenv('WEB_APP_PORT', DEFAULT_WEB_APP_PORT)
    config = uvicorn.Config(configure_app(), host="0.0.0.0", port=int(app_port), log_level="info")
    server = uvicorn.Server(config)
    worker_task = asyncio.create_task(run_worker())

    await server.serve()
    await worker_task


if __name__ == "__main__":
    asyncio.run(main())