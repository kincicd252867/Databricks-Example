"""
Unit tests for My Databricks Project.

This package contains fast, isolated unit tests that don't require a Databricks cluster.
These tests should run quickly and offline.
"""

# Import key test modules to make them easily accessible
from . import test_data_transforms
from . import test_spark_utils

# Define what gets discovered when importing the unit test package
__all__ = [
    'test_data_transforms',
    'test_spark_utils'
]
