from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from redis_msg_bus import order_updates_channel
from config import WEB_APP_PORT
import os
import pathlib
import uvicorn
import asyncio

web_directory = os.path.join(pathlib.Path(__file__).parent.resolve().absolute(), "web")

templates = Jinja2Templates(directory=web_directory)

async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "WEB_APP_PORT":WEB_APP_PORT})

async def order(request: Request):
    order_data = await request.json()
    customer_name = order_data.get("customer_name")
    order_number = "best-coffee-for-{0}".format(str(customer_name).replace(" ","-"))

    return JSONResponse({
        "event_source": "/coffee/order/{0}/status".format(order_number)
    }, status_code=201)

async def order_status(request: Request):
    order_number = request.path_params.get("order_number")
    return EventSourceResponse(
        order_updates_channel(order_number),
        send_timeout=60,
        ping=5,
        ping_message_factory=lambda: ServerSentEvent(**{"comment": "no updates.."})
    )

async def _run_app():
    routes = [
        Route("/", index, methods=["GET"]),
        Route("/coffee/order", order, methods=["POST"]),
        Route("/coffee/order/{order_number}/status", order_status, methods=["GET"]),
        Mount('/static', app=StaticFiles(directory=web_directory))
    ]

    app = CORSMiddleware(
        app=Starlette(routes=routes),
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    config = uvicorn.Config(app, host="0.0.0.0", port=int(WEB_APP_PORT), log_level="info")
    server = uvicorn.Server(config)

    # Run server and keep it running
    await server.serve()

def run_app_process():
    asyncio.run(_run_app())