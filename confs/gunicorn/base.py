import multiprocessing
bind = "127.0.0.1"
port = "8081"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "-"

