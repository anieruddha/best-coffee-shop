import os

TASK_QUEUE = 'counter-service'
TEMPORAL_ADDRESS = os.getenv('TEMPORAL_ADDRESS','localhost:7233')
WEB_APP_PORT = os.getenv('WEB_APP_PORT', 9090)