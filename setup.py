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
    install_requires=["ray[default, data, tune]==2.2.0", "tqdm", "tensorflow~=2.11.0"],
)
