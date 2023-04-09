from setuptools import find_packages, setup

setup(
    name="Reserver",
    version="0.0.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "requests",
    ],
)
