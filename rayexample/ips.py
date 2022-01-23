import time
import ray

ray.init(f"ray://127.0.0.1:10001")

@ray.remote
def f():
    time.sleep(0.01)
    return ray._private.services.get_node_ip_address()

# Get a list of the IP addresses of the nodes that have joined the cluster.
print(set(ray.get([f.remote() for _ in range(1000)])))
