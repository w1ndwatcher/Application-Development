broker_url = "redis://localhost:6379/1"     # queued tasks are stored
result_backend = "redis://localhost:6379/2"     # results of completed tasks are stored
broker_connection_retry_on_startup = True
timezone = "Asia/Kolkata"