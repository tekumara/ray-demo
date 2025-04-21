# sourced from https://github.com/ray-project/ray/blob/9af8f11/doc/kubernetes/example_scripts/run_local_example.py

import sys
import time
from collections import Counter

import ray

""" Run this script locally to execute a Ray program on your Ray cluster on
Kubernetes.

Before running this script, you must port-forward from the local host to
the relevant Kubernetes head service e.g.
kubectl -n ray port-forward service/example-cluster-ray-head 10001:10001.

Set the constant LOCAL_PORT below to the local port being forwarded.
"""
LOCAL_PORT = 10001


@ray.remote
def gethostname(x: tuple[str, ...]) -> tuple[str, ...]:
    import platform
    import time

    time.sleep(0.01)
    return (*x, platform.node())


def wait_for_nodes(expected: int) -> None:
    # Wait for all nodes to join the cluster.
    while True:
        resources = ray.cluster_resources()
        node_keys = [key for key in resources if "node" in key]
        num_nodes = sum(resources[node_key] for node_key in node_keys)
        if num_nodes < expected:
            print(f"{num_nodes} nodes have joined so far, waiting for {expected - num_nodes} more.")
            sys.stdout.flush()
            time.sleep(1)
        else:
            break


def main() -> None:
    wait_for_nodes(2)

    # Check that objects can be transferred from each node to each other node.
    for i in range(10):
        print(f"Iteration {i}")
        results = [gethostname.remote(gethostname.remote(())) for _ in range(100)]
        print(Counter(ray.get(results)))
        sys.stdout.flush()

    print("Success!")
    sys.stdout.flush()


if __name__ == "__main__":
    ray.init(f"ray://127.0.0.1:{LOCAL_PORT}")
    main()
