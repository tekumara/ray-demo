from setuptools import find_packages, setup

setup(
    name="rayexample",
    version="0.0.0",
    description="ray examples",
    python_requires="~=3.9.11",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    # pin protobuf because of https://github.com/ray-project/ray/issues/25282
    install_requires=["ray[data]==1.12.1", "tqdm", "protobuf >= 3.8.0, < 4.0.0"],
)
