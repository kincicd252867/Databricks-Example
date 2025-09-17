#!/bin/bash
# Run integration tests on Databricks

DATABRICKS_HOST=$1
DATABRICKS_TOKEN=$2
VENV_DIR=$3

echo "Running integration tests on Databricks"

# Activate virtual environment
source $VENV_DIR/bin/activate

# Set environment variables for tests
export DATABRICKS_HOST=$DATABRICKS_HOST
export DATABRICKS_TOKEN=$DATABRICKS_TOKEN

# Run integration tests
python -m pytest tests/integration/ -v --cluster-id $DATABRICKS_DEV_CLUSTER_ID

echo "Integration tests completed"
