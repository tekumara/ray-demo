# taken from https://docs.ray.io/en/latest/data/quickstart.html
import numpy as np
import ray

# Load a CSV dataset directly from S3
ds = ray.data.read_csv("s3://anonymous@air-example-data/iris.csv")

# Preview the first record
ds.show(limit=1)


# Define a transformation to compute a "petal area" attribute
def transform_batch(batch: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"]
    vec_b = batch["petal width (cm)"]
    batch["petal area (cm^2)"] = vec_a * vec_b
    return batch


# Apply the transformation to our dataset
transformed_ds = ds.map_batches(transform_batch)

# View the updated schema with the new column
# .materialize() will execute all the lazy transformations and
# materialize the dataset into object store memory
print(transformed_ds.materialize())


# Extract the first 3 rows as a batch for processing
print(transformed_ds.take_batch(batch_size=3))
