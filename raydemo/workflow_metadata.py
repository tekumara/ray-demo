# see https://docs.ray.io/en/latest/workflows/metadata.html#notes

from ray import workflow
import time
import ray
import os

workflow_id = "test"
flagfile = f"/tmp/{workflow_id}"

@ray.remote
def simple():
    open(flagfile, 'a').close()  # touch a file here
    time.sleep(10000)
    return 0

workflow.run_async(simple.bind(), workflow_id=workflow_id)

# make sure workflow step starts running
while not os.path.exists(flagfile):
    time.sleep(1)

workflow_metadata = workflow.get_metadata(workflow_id)
print(workflow_metadata)
assert workflow_metadata["status"] == "RUNNING"
assert "start_time" in workflow_metadata["stats"]
assert "end_time" not in workflow_metadata["stats"]

workflow.cancel(workflow_id)

workflow_metadata = workflow.get_metadata(workflow_id)
print(workflow_metadata)
assert workflow_metadata["status"] == "CANCELED"
assert "start_time" in workflow_metadata["stats"]
assert "end_time" not in workflow_metadata["stats"]
