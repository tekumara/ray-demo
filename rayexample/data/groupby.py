import ray.data
import numpy as np

ds1 = ray.data.range(100).groupby(lambda x: x % 3).count().show()

ds2 = ray.data.from_items([{"A": x % 3, "B": x} for x in range(100)])

ds2.groupby("A").count().show()


ray.data.from_items([(i % 3, i, i**2) for i in range(100)]).groupby(
    lambda x: x[0] % 3
).sum(lambda x: x[2]).show()


# map groups https://docs.ray.io/en/master/data/package-ref.html#ray.data.grouped_dataset.GroupedDataset.map_groups
ds3 = ray.data.range(100).groupby(lambda x: x % 3).map_groups(lambda x: [np.median(x)])
print(ds3.show())
print(ds3.stats())
