# This test is marked to run only if connected to a cluster
pytestmark = pytest.mark.integration

def test_silver_etl_full_job(spark):
    """
    Integration test: Runs the entire Silver ETL logic and validates
    the output table exists and has the expected schema and data quality.
    """
    # Arrange
    test_input_table = "dev.bronze_sales_test"
    test_output_table = "dev.silver_sales_test"
    
    # ... Code to create test input data in `test_input_table` ...
    
    # Act - This simulates what the notebook does
    from my_project.data_transforms import clean_column_names, enforce_schema, add_ingestion_metadata
    raw_df = spark.table(test_input_table)
    cleaned_df = clean_column_names(raw_df)
    conformed_df = enforce_schema(cleaned_df)
    final_df = add_ingestion_metadata(conformed_df)
    final_df.write.format("delta").mode("overwrite").saveAsTable(test_output_table)
    
    # Assert
    # 1. Check table exists
    assert spark.catalog.tableExists(test_output_table), "Output table was not created."
    
    # 2. Check schema has been enforced
    result_df = spark.table(test_output_table)
    assert dict(result_df.dtypes)["sale_amount"] == "double", "Schema enforcement failed."
    
    # 3. Check data quality - no NULLs in a key column
    null_count = result_df.filter(result_df["customer_id"].isNull()).count()
    assert null_count == 0, f"Found {null_count} NULLs in customer_id column."
    
    # 4. Check audit columns were added
    assert "ingestion_timestamp" in result_df.columns, "Audit column missing."
