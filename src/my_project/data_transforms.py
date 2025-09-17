from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def clean_column_names(df: DataFrame) -> DataFrame:
    """
    Cleans column names by lowercasing and replacing spaces.
    This is a pure function, easy to unit test.
    """
    for col_name in df.columns:
        new_name = col_name.lower().replace(' ', '_')
        df = df.withColumnRenamed(col_name, new_name)
    return df

def enforce_schema(df: DataFrame) -> DataFrame:
    """Ensures critical columns have the correct data type."""
    return df.withColumn("sale_amount", df["sale_amount"].cast("double"))

def add_ingestion_metadata(df: DataFrame) -> DataFrame:
    """Adds audit columns to the DataFrame."""
    return df.withColumn("ingestion_timestamp", F.current_timestamp()) \
             .withColumn("ingestion_job_id", F.lit("silver_etl_job"))
