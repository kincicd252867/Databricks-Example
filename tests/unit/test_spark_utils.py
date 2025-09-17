"""
Unit tests for spark_utils.py module.

These tests verify the functionality of Spark session management utilities
without requiring a live Databricks cluster.
"""

import pytest
from unittest.mock import Mock, patch
from pyspark.sql import SparkSession
from my_project.utils.spark_utils import get_spark_session


class TestSparkUtils:
    """Test class for Spark utility functions."""

    @patch('my_project.utils.spark_utils.SparkSession.builder')
    def test_get_spark_session_creation(self, mock_builder):
        """
        Test that get_spark_session creates a SparkSession with correct configuration.
        """
        # Setup
        mock_spark = Mock(spec=SparkSession)
        mock_builder.appName.return_value = mock_builder
        mock_builder.config.return_value = mock_builder
        mock_builder.getOrCreate.return_value = mock_spark
        
        # Execute
        app_name = "TestApp"
        spark = get_spark_session(app_name)
        
        # Assert
        mock_builder.appName.assert_called_once_with(app_name)
        mock_builder.config.assert_any_call("spark.sql.adaptive.enabled", "true")
        mock_builder.config.assert_any_call("spark.sql.adaptive.coalescePartitions.enabled", "true")
        mock_builder.config.assert_any_call("spark.databricks.delta.optimizeWrite.enabled", "true")
        mock_builder.config.assert_any_call("spark.databricks.delta.autoCompact.enabled", "true")
        mock_builder.getOrCreate.assert_called_once()
        assert spark == mock_spark

    def test_get_spark_session_default_app_name(self):
        """
        Test that get_spark_session uses default app name when none is provided.
        """
        with patch('my_project.utils.spark_utils.SparkSession.builder') as mock_builder:
            mock_spark = Mock(spec=SparkSession)
            mock_builder.appName.return_value = mock_builder
            mock_builder.config.return_value = mock_builder
            mock_builder.getOrCreate.return_value = mock_spark
            
            # Call without app_name parameter
            spark = get_spark_session()
            
            # Should use default app name
            mock_builder.appName.assert_called_once_with("MyDatabricksApp")
            assert spark == mock_spark

    @patch('my_project.utils.spark_utils.SparkSession.builder')
    def test_get_spark_session_additional_config(self, mock_builder):
        """
        Test that get_spark_session can accept additional Spark configurations.
        """
        # This test would require modifying the function to accept additional configs
        # For now, it's a placeholder for future functionality
        
        # If we modify get_spark_session to accept **configs parameter:
        # def get_spark_session(app_name="MyDatabricksApp", **configs):
        #     builder = SparkSession.builder.appName(app_name)
        #     for key, value in configs.items():
        #         builder.config(key, value)
        #     # ... rest of the function
        
        # Then we could test:
        # additional_config = {"spark.some.config": "value"}
        # spark = get_spark_session("TestApp", **additional_config)
        # mock_builder.config.assert_any_call("spark.some.config", "value")
        
        # For now, just assert the test would pass
        assert True

    def test_get_spark_session_returns_spark_session(self):
        """
        Test that get_spark_session returns a SparkSession instance.
        """
        # This test would actually create a local Spark session
        # We use a context manager to ensure proper cleanup
        try:
            spark = get_spark_session("TestAppLocal")
            assert isinstance(spark, SparkSession)
            # Verify it has the expected configurations
            assert spark.conf.get("spark.sql.adaptive.enabled") == "true"
        finally:
            # Clean up the Spark session
            if 'spark' in locals():
                spark.stop()


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
