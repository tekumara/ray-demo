# script.py
# copied from https://docs.ray.io/en/latest/cluster/running-applications/job-submission/quickstart.html
import ray


@ray.remote
def hello_world() -> str:
    return "hello world"


# Running on the head node.
# Automatically connect to the running Ray cluster.
ray.init()
print("let's begin!")
print(ray.get(hello_world.remote()))
