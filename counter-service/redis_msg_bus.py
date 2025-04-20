from redis.asyncio import Redis
import os

REQ_PAYMENT = "reqPayment"
COFFEE_READY= "coffeeReady"
ORDER_RECEIVED= "orderReceived"

EVENT_MESSAGES = {
    REQ_PAYMENT : "Your coffee's on its way, pay quickly while Its getting ready.",
    COFFEE_READY: "Your coffee's ready, grab it!",
    ORDER_RECEIVED: "Your coffee's on its way..."
}

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)

redis_client = Redis(host=redis_host, port=redis_port, db=0)

async def notify_request_payment(order_number: str):
    await redis_client.publish(order_number, REQ_PAYMENT)

async def notify_coffee_ready(order_number: str):
    await redis_client.publish(order_number, COFFEE_READY)

async def order_updates_channel(order_number: str):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(order_number)

    yield {
        "event": ORDER_RECEIVED,
        "data": EVENT_MESSAGES.get(ORDER_RECEIVED)
    }

    async for message in pubsub.listen():
        event_key = None
        if message['type'] == 'message':
            cache_key = message.get('data')
            event_key = cache_key.decode('utf-8')
            yield {
                "event": event_key,
                "data": EVENT_MESSAGES.get(event_key)
            }
        if event_key == COFFEE_READY:
            await pubsub.unsubscribe(order_number)
            break