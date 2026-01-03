import multiprocessing

# Workers = (2 x CPU) + 1 is a common formula,
# but for CPU-heavy ML, often 1 worker per core is better to avoid context switching.
workers = multiprocessing.cpu_count()
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
keepalive = 5
timeout = 30  # Fail fast if overloaded
