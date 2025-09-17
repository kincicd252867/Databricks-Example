import pytest
from pyspark.sql import SparkSession
from my_project.data_transforms import clean_column_names, enforce_schema

# Create a Spark session for testing (local mode)
@pytest.fixture(scope='session')
def spark():
    return SparkSession.builder \
        .master("local[1]") \
        .appName("UnitTests") \
        .getOrCreate()

# Test clean_column_names function
def test_clean_column_names(spark):
    # Arrange
    data = [("John Doe", 100)]
    columns = ["Customer Name", "Sale Amount"]
    input_df = spark.createDataFrame(data, columns)
    
    # Act
    result_df = clean_column_names(input_df)
    result_columns = result_df.columns
    
    # Assert
    expected_columns = ["customer_name", "sale_amount"]
    assert result_columns == expected_columns
    assert result_df.collect() == input_df.collect() # Data is unchanged

# Test enforce_schema function
def test_enforce_schema(spark):
    # Arrange
    data = [("100",)]
    columns = ["sale_amount"]
    input_df = spark.createDataFrame(data, columns)
    
    # Act
    result_df = enforce_schema(input_df)
    
    # Assert
    expected_type = 'double'
    actual_type = dict(result_df.dtypes)["sale_amount"]
    assert actual_type == expected_type
