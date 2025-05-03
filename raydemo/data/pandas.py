import pandas as pd
import ray.data


def sum(df: pd.DataFrame) -> pd.DataFrame:
    key = df.iloc[0][0]
    sum = df.sum()["B"] + df.sum()["C"]
    return pd.DataFrame({"key": [key], "sum": [sum]})


df = pd.DataFrame({"A": ["a", "a", "b"], "B": [1, 1, 3], "C": [4, 6, 5]})
ds = ray.data.from_pandas(df)
print(ds.schema())
grouped = ds.groupby("A")
sumdf = grouped.map_groups(sum).to_pandas()
print(sumdf)
