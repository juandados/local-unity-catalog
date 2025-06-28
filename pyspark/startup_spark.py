#!/usr/bin/env python3
"""
IPython startup script to automatically initialize Spark with Unity Catalog configuration.
This script creates a pre-configured Spark session available as 'spark' in all notebooks.
"""

import os
from pyspark.sql import SparkSession

def create_spark_session():
    """Create a Spark session with Unity Catalog configuration."""
    
    # Spark configuration for Unity Catalog
    spark = SparkSession.builder \
        .appName("local-uc-test") \
        .master("local[*]") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.1,io.unitycatalog:unitycatalog-spark_2.12:0.2.1") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "io.unitycatalog.spark.UCSingleCatalog") \
        .config("spark.sql.catalog.unity", "io.unitycatalog.spark.UCSingleCatalog") \
        .config("spark.sql.catalog.unity.uri", "http://server:8080") \
        .config("spark.sql.catalog.unity.token", "") \
        .config("spark.sql.catalog.my_catalog", "io.unitycatalog.spark.UCSingleCatalog") \
        .config("spark.sql.catalog.my_catalog.uri", "http://server:8080") \
        .config("spark.sql.catalog.my_catalog.token", "") \
        .config("spark.sql.defaultCatalog", "unity") \
        .config("spark.databricks.delta.catalog.update.enabled", "true") \
        .getOrCreate()
    
    # Set log level to reduce verbosity
    spark.sparkContext.setLogLevel("WARN")
    
    return spark

# Initialize Spark session
print("🚀 Initializing Spark session with Unity Catalog...")
try:
    spark = create_spark_session()
    print("✅ Spark session initialized successfully!")
    print(f"📊 Spark UI available at: http://localhost:4040")
    print(f"🏗️  Spark version: {spark.version}")
    print(f"📋 Default catalog: {spark.conf.get('spark.sql.defaultCatalog')}")
    
    # Make spark available in the global namespace
    globals()['spark'] = spark
    
    # Also create sc (SparkContext) for convenience
    globals()['sc'] = spark.sparkContext
    
except Exception as e:
    print(f"❌ Failed to initialize Spark session: {e}")
    print("Please check that the Unity Catalog server is running.")
