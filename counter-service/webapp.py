from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from redis_msg_bus import order_updates_channel
from config import WEB_APP_PORT
import os
import pathlib

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

routes = [
    Route("/", index, methods=["GET"]),
    Route("/coffee/order", order, methods=["POST"]),
    Route("/coffee/order/{order_number}/status", order_status, methods=["GET"]),
    Mount('/static', app=StaticFiles( directory=web_directory))
]