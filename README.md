# best-coffe-shop
Temporal.io tutorial in python

- We added orchestrator-service with workflow `CoffeeOrderWorkflow` . 
- `CoffeeOrderWorkflow` executes activity of type `BillCalculationActivity`  to get to know billing amount.

Check related blog posts for more information.


#### Tech Stack :
    docker, 
    docker-compose, 
    python, 
    temporal, 
    SvelteJS - Web UI


#### 📖 Related Blog Posts
- [Brewing Backend Workflows: Setting Up Temporal for Best-Coffee-Shop](https://anieruddha.hashnode.dev/brewing-backend-workflows-setting-up-temporal-for-best-coffee-shop)

- [Brewing Backend Workflows: Your First Temporal Workflow, One Cup at a Time](https://anieruddha.hashnode.dev/temporal-workflow)

- [Brewing Backend Workflows: Setting Up Payment with Temporal Activities](https://anieruddha.hashnode.dev/brewing-backend-workflows-setting-up-payment-with-temporal-activities)

#### Setup
Run `docker-compose up` to create temporal container

#### Diagram

![payment-service-setup.png](assets/payment-service-setup.png)