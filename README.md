# Local Unity Catalog with Delta Lake

This project demonstrates how to use Unity Catalog locally with Delta Lake and PySpark, running in Docker containers.

## Prerequisites

- Docker and Docker Compose
- Git

## Setup and Running

1. **Clone the required repositories:**
   ```sh
   # Clone the forked Delta Lake repository
   git clone https://github.com/juandados/delta.git
   
   # Clone the forked Unity Catalog repository  
   git clone https://github.com/juandados/unitycatalog.git
   ```

2. **Start the services:**
   ```sh
   docker compose up -d
   ```

3. **Access the Spark container:**
   ```sh
   docker exec -it <spark-container-name> bash
   ```

4. **Run PySpark commands inside the container** using the examples below.

---

# PySpark Examples

# Start a new spark session
```sh
pyspark --name "local-uc-test" \
    --master "local[*]" \
    --packages "io.delta:delta-spark_2.12:3.2.1,io.unitycatalog:unitycatalog-spark_2.12:0.2.1" \
    --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
    --conf "spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.unity.uri=http://server:8080" \
    --conf "spark.sql.catalog.unity.token=" \
    --conf "spark.sql.catalog.my_catalog=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.my_catalog.uri=http://server:8080" \
    --conf "spark.sql.catalog.my_catalog.token=" \
    --conf "spark.sql.defaultCatalog=unity" \
    --conf "spark.databricks.delta.catalog.update.enabled=true" #needed to write the columns in unity
```

## List schemas in catalog unity

```python
# List all schemas in the unity catalog
spark.sql("SHOW SCHEMAS IN unity").show()
```

## Show tables in default schema

```python
# Show all tables in the default schema
spark.sql("SHOW TABLES IN unity.default").show()
```
## Show location of unity.default delta table

```python
# Show the location of the delta table on disk
spark.sql("DESCRIBE DETAIL unity.default.numbers").show(truncate=False)
```

## Show metadata location for unity.default.numbers

```python
# Show where the metadata for the delta table is stored
spark.sql("DESCRIBE EXTENDED unity.default.numbers").show(truncate=False)
```

## Show records in unity.default.marksheet

```python
# Show all records from the marksheet table
spark.sql("SELECT * FROM unity.default.numbers").show()
```

## Create a new table called employees in unity.default

```python
# Create a new employees table in unity.default
spark.sql("""
CREATE TABLE unity.default.employees1 (
    employee_id INT COMMENT 'Unique identifier for each employee',
    first_name STRING COMMENT 'Employee first name',
    last_name STRING COMMENT 'Employee last name',
    email STRING COMMENT 'Employee email address',
    department STRING COMMENT 'Department where employee works',
    hire_date TIMESTAMP COMMENT 'Date when employee was hired',
    salary DOUBLE COMMENT 'Employee annual salary in USD'
) USING DELTA
LOCATION '/home/unitycatalog/etc/data/external/unity/default/tables/employees1'
""")
```
## Write employees table to MinIO S3 path

```python
# Write the employees table to a MinIO S3 path
spark.sql("""
CREATE TABLE unity.default.employees_backup
USING DELTA
LOCATION 's3a://bk1/employees_backup'
AS SELECT * FROM unity.default.employees
""")
```

## Write DataFrame to MinIO S3 as Parquet

```python
# Read table and write to MinIO as Parquet
df = spark.table("unity.default.employees")
df.write.mode("overwrite").parquet("s3a://warehouse/unity/default/exports/employees_parquet")
```

## Write DataFrame to MinIO S3 as Delta

```python
# Read table and write to MinIO as Delta format
df = spark.table("unity.default.employees")
df.write.format("delta").mode("overwrite").save("s3a://warehouse/unity/default/exports/employees_delta")
```
## Insert sample data into unity.default.employees

```python
# Insert mock employee data
spark.sql("""
INSERT INTO unity.default.employees1 VALUES
(1, 'John', 'Doe', 'john.doe@company.com', 'Engineering', '2023-01-15', 75000.00),
(2, 'Jane', 'Smith', 'jane.smith@company.com', 'Marketing', '2023-02-20', 68000.00),
(3, 'Mike', 'Johnson', 'mike.johnson@company.com', 'Sales', '2023-03-10', 72000.00),
(4, 'Sarah', 'Wilson', 'sarah.wilson@company.com', 'HR', '2023-01-25', 65000.00),
(5, 'David', 'Brown', 'david.brown@company.com', 'Engineering', '2023-04-05', 80000.00)
""")
```

## Show records in unity.default.employees

```python
# Show all records from the employees table
spark.sql("SELECT * FROM unity.default.employees").show()
```
# Using MinIO S3
## Start a new spark session with MinIO S3 configuration
```sh
pyspark --name "local-uc-test" \
    --master "local[*]" \
    --packages "io.delta:delta-spark_2.12:3.2.1,io.unitycatalog:unitycatalog-spark_2.12:0.2.0,org.apache.hadoop:hadoop-aws:3.3.4" \
    --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
    --conf "spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.unity.uri=http://server:8080" \
    --conf "spark.sql.catalog.unity.token=" \
    --conf "spark.sql.catalog.my_catalog=io.unitycatalog.spark.UCSingleCatalog" \
    --conf "spark.sql.catalog.my_catalog.uri=http://server:8080" \
    --conf "spark.sql.catalog.my_catalog.token=" \
    --conf "spark.sql.defaultCatalog=unity" \
    --conf "spark.hadoop.fs.s3.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" \
    --conf "spark.hadoop.fs.s3a.endpoint=http://minio:9000" \
    --conf "spark.hadoop.fs.s3a.access.key=minioadmin" \
    --conf "spark.hadoop.fs.s3a.secret.key=minioadmin" \
    --conf "spark.hadoop.fs.s3a.path.style.access=true" \
    --conf "spark.hadoop.fs.s3a.connection.ssl.enabled=false"
```
## Create external Delta table from CSV in MinIO S3

```python
# Read CSV from MinIO S3 and create DataFrame
df_csv = spark.read.option("header", "true").option("sep", ",").csv("s3a://bk1/username.csv")

# Create a temporary view from the cleaned CSV data
df_csv.createOrReplaceTempView("username_temp_view")

# Get the schema from the username_temp_view
spark.sql("DESCRIBE username_temp_view").show()

# Alternative: Print schema in a more readable format
df_csv.printSchema()

# Alternative: Get schema as a string
schema_string = df_csv.schema.simpleString()
print(f"Schema: {schema_string}")

# Alternative: Get detailed schema information
spark.sql("DESCRIBE EXTENDED username_temp_view").show(truncate=False)

# Create the table using UC Server API using the user_temp_view schema
# Then insert data in table from the view instead of Create a Delta table from the CSV data
spark.sql("""
CREATE TABLE unity.default.username_delta
USING DELTA
LOCATION '/home/unitycatalog/etc/data/external/unity/default/tables/username_delta'
AS SELECT * FROM username_temp_view
""")
```

# Create a Table 
```sh
curl -X POST http://localhost:8080/api/2.1/unity-catalog/tables \
  -H "Content-Type: application/json" \
  -d '{
    "name": "external_customers",
    "catalog_name": "unity",
    "schema_name": "default",
    "table_type": "EXTERNAL",
    "data_source_format": "DELTA",
    "storage_location": "/home/unitycatalog/etc/data/external/unity/default/tables/external_customers",
    "columns": [
      {
        "name": "customer_id",
        "type_text": "INT",
        "type_json": "{\"type\":\"integer\"}",
        "type_name": "INT",
        "type_precision": 0,
        "type_scale": 0,
        "position": 0,
        "comment": "Customer ID",
        "nullable": false
      },
      {
        "name": "customer_name",
        "type_text": "STRING",
        "type_json": "{\"type\":\"string\"}",
        "type_name": "STRING",
        "type_precision": 0,
        "type_scale": 0,
        "position": 1,
        "comment": "Customer name",
        "nullable": true
      },
      {
        "name": "email",
        "type_text": "STRING",
        "type_json": "{\"type\":\"string\"}",
        "type_name": "STRING",
        "type_precision": 0,
        "type_scale": 0,
        "position": 2,
        "comment": "Customer email",
        "nullable": true
      }
    ],
    "comment": "External customers table stored on local filesystem"
  }'
```
```py
spark.sql("""
CREATE TABLE unity.default.external_tables USING DELTA
LOCATION '/home/unitycatalog/etc/data/external/unity/default/tables/external_customers'
""")
```
## Using sql statement
```python
spark.sql("""
INSERT INTO unity.default.external_customers VALUES
(1, 'John', 'Doe'),
(2, 'Jane', 'Smith'),
(3, 'Mike', 'Johnson'),
(4, 'Sarah', 'Wilson'),
(5, 'David', 'Brown')
""")
```