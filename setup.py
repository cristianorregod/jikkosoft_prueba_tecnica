from setuptools import setup, find_packages

setup(
    name="customer-analytics",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.2",
        "pytest-cov>=4.1.0",
    ],
)