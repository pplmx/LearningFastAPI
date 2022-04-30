import multiprocessing

bind = '0.0.0.0:8080'
worker_class = 'uvicorn.workers.UvicornWorker'

workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2
