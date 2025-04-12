from temporalio import workflow
from datetime import timedelta
from dataclasses import dataclass
from temporal_config import TASK_QUEUE


@dataclass  
class CoffeeOrder:
	customer_name: str
	order_number: str
	quantity: int = 1  
  

@workflow.defn(name="CoffeeOrderWorkflow")
class CoffeeOrderWorkflow:
	@workflow.run
	async def run(self, order: CoffeeOrder):
		workflow.logger.info("CoffeeOrderWorkflow : we soon be serving coffee.. Order : {0}".format(order))
		result = await workflow.execute_activity("BillCalculationActivity",  order, task_queue='payment-service', start_to_close_timeout=timedelta(seconds=15))

		return result