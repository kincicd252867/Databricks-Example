#!/bin/bash
# Deploy project to Databricks

DATABRICKS_HOST=$1
DATABRICKS_TOKEN=$2
WHEEL_PATH=$3
PROJECT_VERSION=$4
ENVIRONMENT=$5

echo "Deploying to Databricks $ENVIRONMENT environment"

# Install Databricks CLI
pip install databricks-cli

# Configure Databricks CLI
echo "Configuring Databricks CLI for $ENVIRONMENT"
databricks configure --token --host $DATABRICKS_HOST <<EOF
$DATABRICKS_TOKEN
EOF

# Upload notebooks
echo "Uploading notebooks to Databricks workspace"
databricks workspace import_dir ./notebooks /Shared/$ENVIRONMENT/my-project --overwrite

# Upload wheel library to DBFS
echo "Uploading wheel package to DBFS"
databricks fs cp --overwrite $WHEEL_PATH "dbfs:/FileStore/wheels/my_project-$PROJECT_VERSION-py3-none-any.whl"

# Install library on cluster (assuming cluster ID is available as environment variable)
if [ "$ENVIRONMENT" = "dev" ]; then
    CLUSTER_ID=$DATABRICKS_DEV_CLUSTER_ID
else
    CLUSTER_ID=$DATABRICKS_PROD_CLUSTER_ID
fi

echo "Installing library on cluster $CLUSTER_ID"
databricks libraries install \
    --cluster-id $CLUSTER_ID \
    --whl "dbfs:/FileStore/wheels/my_project-$PROJECT_VERSION-py3-none-any.whl"

# Deploy job configuration
echo "Deploying job configuration"
databricks jobs create --json-file databricks-resources/job_configs/silver_etl_job.json || \
databricks jobs reset --job-id $(databricks jobs list --output json | jq -r '.jobs[] | select(.settings.name == "Silver_Sales_ETL_Job").job_id') --json-file databricks-resources/job_configs/silver_etl_job.json

echo "Deployment to $ENVIRONMENT completed successfully"
