from temporalio import activity
from dataclasses import dataclass

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


@activity.defn(name='BrewCoffeeActivity')
async def brew_coffee(supplies: Supplies) -> ReadyCoffeeOrder:
    activity.logger.info("Brewing coffee with CoffeeBeans = {0} & sugar = {1}".format(supplies.coffee_beans, supplies.suger))
    activity.logger.info("Now filling coffee in {0} cups".format(supplies.cups))

    return ReadyCoffeeOrder(
        supplies.order_number,
        supplies.cups
    )