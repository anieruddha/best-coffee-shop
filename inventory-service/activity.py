from temporalio import activity
from dataclasses import dataclass

@dataclass
class CoffeeOrder:
    customer_name: str
    order_number: str
    quantity: int = 1

@dataclass
class Supplies:
    order_number: str
    cups: int
    coffee_beans: int
    suger: int

CUP_FOR_COFFEE = 1
COFFEE_BEANS_PER_COFFEE = 25
SUGER_PER_COFFEE = 1

@activity.defn(name='GetSuppliesActivity')
async def get_supplies(order: CoffeeOrder) -> Supplies:
    no_of_coffee = order.quantity
    return Supplies(
        order.order_number,
        CUP_FOR_COFFEE * no_of_coffee,
        COFFEE_BEANS_PER_COFFEE * no_of_coffee,
        SUGER_PER_COFFEE * no_of_coffee
    )
