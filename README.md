# Local Unity Catalog with Delta Lake

This project demonstrates how to use Unity Catalog locally with Delta Lake and PySpark, running in Docker containers.

## Prerequisites

- Git
- Docker and Docker Compose

## Setup and Running

1. **Clone the required repositories:**
   ```sh
   # Clone the main repository
   git clone https://github.com/juandados/local-unity-catalog.git
   cd local-unity-catalog

   # Clone the forked Unity Catalog repository  
   git clone https://github.com/juandados/unitycatalog.git

   # Clone the forked Delta Lake repository
   git clone https://github.com/juandados/delta.git
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

**Note** You should have spark 3.5.3 or above to support unitycatalog features.

## Start a new spark session
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
    --conf "spark.databricks.delta.catalog.update.enabled=true"
```

**Note:** Replace `server` by `localhost` when working with the delta container within the client compose.

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
# Drop the employees table if it exists
spark.sql("DROP TABLE IF EXISTS unity.default.employees")
```

## Create a new table called employees in unity.default

```python
# Create a new employees table in unity.default
spark.sql("""
CREATE TABLE unity.default.employees (
    employee_id INT COMMENT 'Unique identifier for each employee',
    first_name STRING COMMENT 'Employee first name',
    last_name STRING COMMENT 'Employee last name',
    email STRING COMMENT 'Employee email address',
    department STRING COMMENT 'Department where employee works',
    hire_date TIMESTAMP COMMENT 'Date when employee was hired',
    salary DOUBLE COMMENT 'Employee annual salary in USD'
) USING DELTA
LOCATION '/home/unitycatalog/etc/data/external/unity/default/tables/employees'
""")
```

## Insert sample data into unity.default.employees

```python
# Insert mock employee data
spark.sql("""
INSERT INTO unity.default.employees VALUES
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
## Read as a Spark-DataFrame.

```python
df = spark.table("unity.default.employees")
df.show()
```
