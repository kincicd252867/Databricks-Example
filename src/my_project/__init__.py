"""
My Databricks Project

A package containing data transformation utilities and helpers for Databricks ETL workflows.
"""

__version__ = "1.0.0"
__author__ = "Data Engineering Team"
__description__ = "Databricks ETL transformation utilities"

# Import key functions to make them available at package level
from .data_transforms import (
    clean_column_names,
    enforce_schema,
    add_ingestion_metadata
)

# Define what gets imported with "from my_project import *"
__all__ = [
    'clean_column_names',
    'enforce_schema',
    'add_ingestion_metadata',
    'utils'  # This makes the utils subpackage available
]
