# Databricks notebook source
# This is how Databricks adds magic commands when exporting to .py
# MAGIC %md
# MAGIC # Silver Layer ETL
# MAGIC This notebook transforms raw bronze data into a silver layer.

# COMMAND ----------

# Import custom modules from our packaged code
from my_project.data_transforms import clean_column_names, enforce_schema, add_ingestion_metadata
from my_project.utils.spark_utils import get_spark_session

# COMMAND ----------

# Read raw (bronze) data
raw_df = spark.table("bronze_sales")

# COMMAND ----------

# Apply transformations using our centralized logic
cleaned_df = clean_column_names(raw_df)
conformed_df = enforce_schema(cleaned_df)
final_df = add_ingestion_metadata(conformed_df)

# COMMAND ----------

# Write to Delta Lake silver table
final_df.write.format("delta").mode("overwrite").saveAsTable("silver_sales")
