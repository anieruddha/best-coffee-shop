from temporalio import workflow
from datetime import timedelta
from dataclasses import dataclass


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
		workflow.sleep(120)