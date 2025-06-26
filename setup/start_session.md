# 🌟 Unity Catalog with Local PySpark 🌟

This project enables working with Unity Catalog locally using PySpark and Delta Lake.

## 🚀 Quick Start

To initialize the Spark session properly with Unity Catalog:

### 1️⃣ Clean up environment variables

```python
import os
if "SPARK_REMOTE" in os.environ:
    del os.environ["SPARK_REMOTE"]
if "SPARK_LOCAL" in os.environ:
    del os.environ["SPARK_LOCAL"]
```

## 2️⃣ Temporarily disable Databricks Connect validations

```python
try:
    from pyspark.sql import SparkSession
    if hasattr(SparkSession.Builder, "_validate_startup_urls"):
        original_method = SparkSession.Builder._validate_startup_urls
        SparkSession.Builder._validate_startup_urls = lambda self: None
except Exception:
    pass
```

## 3️⃣ Create the Spark session

```python
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
    .enableHiveSupport() \
    .getOrCreate()
```

## 4️⃣ Restore original method if it was modified

```python
try:
    if "original_method" in locals():
        SparkSession.Builder._validate_startup_urls = original_method
except:
    pass
```

## 🔍 Example Queries
Once the session is initialized, run queries like:

```python
# 📊 List all available catalogs
spark.sql('SHOW CATALOGS').show()
# 📋 Show tables in the default schema
spark.sql("SHOW TABLES IN unity.default").show()
# 📝 Describe a specific table
spark.sql("DESCRIBE EXTENDED unity.default.employees").show(truncate=False)
# 📈 Load a table as a DataFrame
df = spark.table("unity.default.employees")
df.show()
```

## 🛠️ Requirements

- Docker
- Docker Compose
- PySpark 3.5.x
- Unity Catalog 0.2.1

## 📦 Project Structure

- `server`: Unity Catalog backend server
- `ui`: Web UI for managing Unity Catalog
- `pyspark`: Local PySpark environment with all dependencies

## 🔒 Important Notes

- This configuration temporarily disables some Databricks Connect validations to enable local use.
- Ideal for development and testing — not recommended for production.
- All catalogs and data are local and non-persistent by default.

## 🤝 Contributions

- Contributions are welcome! Open an issue or pull request for suggestions or improvements.

## 📄 Licencia

MIT