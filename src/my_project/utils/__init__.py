"""
Utility functions for My Databricks Project

This subpackage contains helper utilities for Spark operations and other common tasks.
"""

from .spark_utils import get_spark_session

# Define what gets imported with "from my_project.utils import *"
__all__ = [
    'get_spark_session'
]
