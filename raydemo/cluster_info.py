import socket
import time
from collections import Counter

import ray

ray.init(address="ray://127.0.0.1:10001")
print(f"{ray.__version__} {ray.__commit__}")

print(
    """This cluster consists of
    {} nodes in total
    {} CPU resources in total
    {} memory resources in total
""".format(
        len([n for n in ray.nodes() if n["Alive"]]), ray.cluster_resources()["CPU"], ray.cluster_resources()["memory"]
    )
)


@ray.remote
def f() -> str:
    time.sleep(0.001)
    # Return IP address.
    return socket.gethostbyname("localhost")


object_ids = [f.remote() for _ in range(10000)]
ip_addresses = ray.get(object_ids)

print("Tasks executed")
for ip_address, num_tasks in Counter(ip_addresses).items():
    print(f"    {num_tasks} tasks on {ip_address}")
