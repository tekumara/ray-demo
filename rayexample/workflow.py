# see https://docs.ray.io/en/latest/workflows/basics.html

from ray import workflow
from typing import List

@workflow.step
def read_data(num: int):
    return [i for i in range(num)]

@workflow.step
def preprocessing(data: List[float]) -> List[float]:
    return [d**2 for d in data]

@workflow.step
def aggregate(data: List[float]) -> float:
    return sum(data)

# Initialize workflow storage.
workflow.init()

# Setup the workflow.
data = read_data.step(10)
preprocessed_data = preprocessing.step(data)
output = aggregate.step(preprocessed_data)

# Execute the workflow and print the result.
print(output.run())

# The workflow can also be executed asynchronously.
# print(ray.get(output.run_async()))

# List all workflows run in the cluster and their state
print(workflow.list_all())
