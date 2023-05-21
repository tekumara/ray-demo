from setuptools import find_packages, setup

setup(
    name="raydemo",
    version="0.0.0",
    description="ray examples",
    python_requires="~=3.10.10",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    install_requires=[
        "ray[default, data, tune]==2.4.0",
        "tqdm",
        "tensorflow~=2.11.0; sys_platform != 'darwin' or platform_machine != 'arm64'",
        "tensorflow-macos~=2.11.0; sys_platform == 'darwin' and platform_machine == 'arm64'"
    ],
)
