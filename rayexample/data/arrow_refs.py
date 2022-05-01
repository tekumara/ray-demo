# create a dataset from arrow refs so data isn't pulled to the client

import ray
import pyarrow as pa


@ray.remote
class DataGenerator:
    def generate_data(self):
        return pa.table({"a": [1, 2, 3], "b": [4, 5, 6]})


data_generator = DataGenerator.remote()
refs = [data_generator.generate_data.remote() for _ in range(5)]

ds = ray.data.from_arrow_refs(refs)

# materialize
ds.show()
