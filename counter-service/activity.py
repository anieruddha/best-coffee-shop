from temporalio import activity
from dataclasses import dataclass
from redis_msg_bus import notify_request_payment, notify_coffee_ready

@dataclass
class OrderBill:
    order_number: str
    amount: int

@dataclass
class BrewedCoffee:
    order_number: str
    num_of_coffees: int

@activity.defn(name='RequestPaymentActivity')
async def request_payment(bill: OrderBill) :
    await notify_request_payment(bill.order_number)

@activity.defn(name='ServeCoffeeActivity')
async def serve_coffee(coffee: BrewedCoffee) :
    await notify_coffee_ready(coffee.order_number)