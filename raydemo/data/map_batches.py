import ray.data

# Create a dataset and then create a pipeline from it.
base = ray.data.range(1000000)
print(base)
# -> Dataset(num_blocks=200, num_rows=1000000, schema=<class 'int'>)
pipe = base.window(blocks_per_window=10)
print(pipe)
# -> DatasetPipeline(num_windows=20, num_stages=1)

# Applying transforms to pipelines adds more pipeline stages.
# map_batches are applied in parallel
pipe = pipe.map_batches(lambda batch: [v * 2 for v in batch])
print(pipe)

num_rows = 0
for _ in pipe.iter_rows():
    num_rows += 1  # noqa: SIM113
