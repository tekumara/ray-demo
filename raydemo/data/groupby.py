import numpy as np
import pandas as pd
import ray.data

ds1 = ray.data.range(100).groupby(lambda x: x % 3).count().show()

ds2 = ray.data.from_items([{"A": x % 3, "B": x} for x in range(100)])

ds2.groupby("A").count().show()


ray.data.from_items([(i % 3, i, i**2) for i in range(100)]).groupby(lambda x: x[0] % 3).sum(lambda x: x[2]).show()


# return type must be of type Block, here we use List
def median(x: list[int]) -> list[np.float64]:
    return [np.median(x)]


# map groups https://docs.ray.io/en/latest/data/api/doc/ray.data.grouped_dataset.GroupedDataset.map_groups.html
ds3 = ray.data.range(100).groupby(lambda x: x % 3).map_groups(median)  # type: ignore see https://github.com/ray-project/ray/issues/35577

print(ds3.show())


def sum(df: pd.DataFrame) -> pd.DataFrame:
    key = df.iloc[0][0]
    sum = df.sum()["B"] + df.sum()["C"]
    return pd.DataFrame({"key": [key], "sum": [sum]})


df = pd.DataFrame({"A": ["a", "a", "b"], "B": [1, 1, 3], "C": [4, 6, 5]})
ds = ray.data.from_pandas(df)
grouped = ds.groupby("A")
sumdf = grouped.map_groups(sum).to_pandas()
print(sumdf)
