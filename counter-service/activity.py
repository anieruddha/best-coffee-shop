from temporalio import activity
from dataclasses import dataclass

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
    activity.logger.info("Hi please pay {0} to proceed".format(bill.amount))

@activity.defn(name='ServeCoffeeActivity')
async def serve_coffee(coffee: BrewedCoffee) :
    activity.logger.info("Thank you, enjoy your cofee {0} ".format(coffee))


