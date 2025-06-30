"""
Unity Catalog and Delta Lake Examples

This script demonstrates basic operations with Unity Catalog and Delta Lake:
- Querying catalogs and tables
- Inserting data into tables
- Using time travel features to access specific versions
- Exporting data to CSV and Parquet formats

Requirements:
- Configured Spark environment with Unity Catalog access
- 'employees' table in unity.default schema
"""
# Display all available catalogs in Unity Catalog
spark.sql("SHOW CATALOGS").show()
# Show tables in the default schema of unity catalog
spark.sql("SHOW TABLES IN unity.default").show()
# Try to describe the employees table, otherwise guide the user
try:
    # Show detailed structure of the employees table
    spark.sql("DESCRIBE EXTENDED unity.default.employees").show(truncate=False)
    # Show a preview of the data in the table
    spark.sql("SELECT * FROM unity.default.employees").show()
except Exception as e:
    print(f"Error describing table: {e}")
    print("Please read the README.md and/or run explore_jupyter_session.py to configure your environment.")

# Write in employees table
spark.sql("""
INSERT INTO unity.default.employees VALUES
(1, 'John', 'Doe', 'john.doe@company.com', 'Engineering', '2023-01-15', 75000.00),
(2, 'Jane', 'Smith', 'jane.smith@company.com', 'Marketing', '2023-02-20', 68000.00),
(3, 'Mike', 'Johnson', 'mike.johnson@company.com', 'Sales', '2023-03-10', 72000.00),
(4, 'Sarah', 'Wilson', 'sarah.wilson@company.com', 'HR', '2023-01-25', 65000.00),
(5, 'David', 'Brown', 'david.brown@company.com', 'Engineering', '2023-04-05', 80000.00)
""")

spark.sql("DESCRIBE EXTENDED unity.default.employees").show(truncate=False)
spark.sql("SELECT * FROM unity.default.employees").show()

# Version 0 - Create table
(
    spark
    .read
    .format("delta")
    .option("versionAsOf", 0)
    .table("unity.default.employees")
    .show(truncate=False)
)

# Version 1 - Firts read in table
(
    spark
    .read
    .format("delta")
    .option("versionAsOf", 1)
    .table("unity.default.employees")
    .show(truncate=False)
)

# Write in employees table (New version)
spark.sql("""
INSERT INTO unity.default.employees VALUES
  (6, 'Cars', 'Doe',   'cars.doe@company.com',   'Marketing', '2023-01-15',  52000.00),
  (7, 'Janet', 'Smith', 'janet.smith@company.com', 'Marketing', '2023-02-20', 168000.00),
  (8, 'Mike',  'Carson','mike.carson@company.com','Engineering','2023-03-10',  72000.00),
  (9, 'Sarah', 'Wilson','sarah.wilson@company.com','HR',         '2023-01-25',  73000.00),
  (10,'David', 'Yellow','david.yellow@company.com','Engineering','2023-04-05',  80000.00)
""")

spark.sql("DESCRIBE EXTENDED unity.default.employees").show(truncate=False)


# Last version
print("==============================")
print("last version, employees table:")
print("==============================")
spark.sql("SELECT * FROM unity.default.employees").show(truncate=False)

# Version 0
print("============================")
print("Version 0, employees table:")
print("============================")
(
    spark
    .read
    .format("delta")
    .option("versionAsOf", 0)
    .table("unity.default.employees")
    .show(truncate=False)
)

# Version 1
print("============================")
print("Version 1, employees table:")
print("============================")
(
    spark
    .read
    .format("delta")
    .option("versionAsOf", 1)
    .table("unity.default.employees")
    .show(truncate=False)
)

# Version 2
print("============================")
print("Version 2, employees table:")
print("============================")
(
    spark
    .read
    .format("delta")
    .option("versionAsOf", 2)
    .table("unity.default.employees")
    .show(truncate=False)
)

# Convert Spark DataFrame to Pandas and display its content
df = spark.sql("SELECT * FROM unity.default.employees")
df.write.mode("overwrite").option("header", "true").csv("download/employees_spark.csv")  # Save DataFrame as CSV, overwriting if it already exists

# Save Pandas DataFrame as Parquet file without including the index
print(df.toPandas())
df.toPandas().to_parquet("download/employees_pandas.parquet", index=False)
