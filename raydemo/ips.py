import time

import ray

ray.init()


@ray.remote
def f() -> str:
    time.sleep(0.01)
    return ray._private.services.get_node_ip_address()  # type: ignore # noqa: SLF001


# Get a list of the IP addresses of the nodes that have joined the cluster.
print(set(ray.get([f.remote() for _ in range(1000)])))
