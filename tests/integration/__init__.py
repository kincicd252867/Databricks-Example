"""
Integration tests for My Databricks Project.

This package contains slower integration tests that require a connection to a Databricks cluster.
These tests validate the complete workflow in a real environment.
"""

# Import key test modules to make them easily accessible
from . import test_silver_etl_integration

# Define what gets discovered when importing the integration test package
__all__ = [
    'test_silver_etl_integration'
]
