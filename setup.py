from setuptools import find_packages, setup

setup(
    name="rayexample",
    version="0.0.0",
    description="ray examples",
    python_requires="~=3.7.7",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    install_requires=["ray[data]~=1.9", "tqdm~=4.62"],
)
