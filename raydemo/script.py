# script.py
# copied from https://docs.ray.io/en/latest/cluster/running-applications/job-submission/quickstart.html
import ray


@ray.remote
def hello_world() -> str:
    return "hello world"


# Automatically connect to the running Ray cluster.
ray.init()
print(ray.get(hello_world.remote()))
