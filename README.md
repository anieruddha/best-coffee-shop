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
    HTML + JavaSCript + SSE


#### 📖 Related Blog Posts

[Brewing Coffee : Setting Up Temporal for Best-Coffee-Shop](https://anieruddha.hashnode.dev/temporal-tutorial-docker-setup)

[Brewing Coffee : First Temporal Workflow, One Cup at a Time](https://anieruddha.hashnode.dev/temporal-tutorial-first-workflow)

[Brewing Backend Workflows: Setting Up Payment with Temporal Activities](https://anieruddha.hashnode.dev/temporal-tutorial-first-activity)

[Brewing Coffee : Setting up remaining Activities](https://anieruddha.hashnode.dev/brewing-coffee-setting-up-remaining-activities)

### Setup
1. Run `docker-compose up` to run all containers.

### System Walkthrough

#### 1. Start the System
Make sure all containers are up and running using:

```bash
docker-compose up
```

#### 2. Place order using browser
Go to `http://localhost:9090` to place order
   - ##### Options for coffee type and quantity are intentionally disabled.  To place order simply put your name
   - Once order placed
     - The backend establishes a Server-Sent Events (SSE) connection using the EventSource API.
     - The frontend listens for following events:
       - reqPayment - it will show message about required payment
       - coffeeReady - it will show coffee ready message & close SSE connection

#### 3. Connect to Redis to simluate payment request & coffee ready message
Connect to redis in different terminal using
```bash
redis-cli
```
In the Redis CLI, run the following command to list all current pub/sub channels:
```bash
PUBSUB CHANNELS
```
You should see a channel named like: `best-coffee-for-<your-name>`. This channel is dynamically created based on the customer’s name and used for streaming live order updates to their session.

To simulate a payment request: 
```bash
PUBLISH best-coffee-for-<your-name> reqPayment
```
To simulate that the coffee is ready:
```bash
PUBLISH best-coffee-for-<your-name> coffeeReady
```

#### Once coffeeReady is published:
- The backend unsubscribes from the Redis channel. 
- The SSE stream to the frontend is closed. 
- The customer sees a final notification that their order is ready.

