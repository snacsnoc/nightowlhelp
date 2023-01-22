from rq import Worker, Queue, Connection


import redis
import os

# get url, set default
# "redis://localhost:6379"
redis_url = os.getenv(
    "REDIS_URL",
    "rediss://:password@redisurl:30992",
)


conn = redis.StrictRedis(
    host="redisurl",
    port=30992,
    password="password",
    ssl=True,
    ssl_ca_certs="./select-ssl-cert.pem",
)

if __name__ == "__main__":
    # A context has an __enter__ method, executed on entry and an __exit__ method, executed on exit
    with Connection(conn):
        q = Queue(connection=conn)
        worker = Worker(queues=[q], connection=conn)
        worker.work(with_scheduler=True)
