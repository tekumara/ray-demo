# create a dataset from arrow refs so data isn't pulled to the client

import pyarrow as pa
import ray.data


@ray.remote
class DataGenerator:
    def generate_data(self) -> pa.Table:
        return pa.table({"a": [1, 2, 3], "b": [4, 5, 6]})


data_generator = DataGenerator.remote()
refs = [
    data_generator.generate_data.remote()
    for _ in range(5)  # pyright: ignore[reportAttributeAccessIssue] see https://github.com/ray-project/ray/issues/50410
]

ds = ray.data.from_arrow_refs(refs)

# materialize
ds.show()
