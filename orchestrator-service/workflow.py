from temporalio import workflow
from datetime import timedelta
from dataclasses import dataclass
from temporal_config import TASK_QUEUE

@dataclass  
class CoffeeOrder:
	customer_name: str
	order_number: str
	quantity: int = 1

@dataclass
class OrderBill:
	order_number: str
	amount: int

@dataclass
class Supplies:
	order_number: str
	cups: int
	coffee_beans: int
	suger: int

@dataclass
class ReadyCoffeeOrder:
	order_number: str
	num_of_coffees: int

@workflow.defn(name="CoffeeOrderWorkflow")
class CoffeeOrderWorkflow:
	@workflow.run
	async def run(self, order: CoffeeOrder):
		# Calculate Payment
		payment_info: OrderBill = await workflow.execute_activity("BillCalculationActivity",  order, task_queue="payment-service", start_to_close_timeout=timedelta(seconds=15))

		# Request Payment
		await workflow.execute_activity("RequestPaymentActivity", payment_info, task_queue="counter-service", start_to_close_timeout=timedelta(seconds=15))

		# Collect Supplies
		coffee_supplies: Supplies = await workflow.execute_activity("GetSuppliesActivity", order, task_queue="inventory-service", start_to_close_timeout=timedelta(seconds=15))

		# Brew Coffee
		ready_order: ReadyCoffeeOrder = await workflow.execute_activity("BrewCoffeeActivity", coffee_supplies, task_queue="brewing-service", start_to_close_timeout=timedelta(seconds=15))

		# Serve Coffee
		await workflow.execute_activity("ServeCoffeeActivity", ready_order, task_queue="counter-service", start_to_close_timeout=timedelta(seconds=15))