from temporalio import activity
from dataclasses import dataclass

@dataclass
class CoffeeOrder:
    customer_name: str
    order_number: str
    quantity: int = 1

@dataclass
class OrderBill:
    order_number: str
    amount: int

COFFEE_UNIT_PRICE = 2000

@activity.defn(name='BillCalculationActivity')
async def calculate_payment(order: CoffeeOrder) -> OrderBill:
    bill_amount = order.quantity * COFFEE_UNIT_PRICE
    return OrderBill(
        order_number=order.order_number,
        amount=bill_amount
    )
