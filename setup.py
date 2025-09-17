from setuptools import setup, find_packages

setup(
    name="my-databricks-project",
    version="1.0.0",
    description="Custom transformations for Databricks ETL",
    author="Data Engineering Team",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyspark>=3.5.0'
    ],
)v
