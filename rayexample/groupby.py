import ray

ds1 = ray.data.range(100).groupby(lambda x: x % 3).count().show()

ds2 = ray.data.from_items([{"A": x % 3, "B": x} for x in range(100)])

ds2.groupby("A").count().show()


ray.data.from_items([(i % 3, i, i**2) for i in range(100)]).groupby(lambda x: x[0] % 3).sum(lambda x: x[2]).show()
