# Display all available catalogs in Unity Catalog
spark.sql("SHOW CATALOGS").show()
# Show tables in the default schema of unity catalog
spark.sql("SHOW TABLES IN unity.default").show()
# Show detailed structure of the employees table
spark.sql("DESCRIBE EXTENDED unity.default.employees").show(truncate=False)
# Load employees table into a Spark DataFrame
df = spark.table("unity.default.employees")
# Show a preview of the data in the table
df.show()

# Convert Spark DataFrame to Pandas and display its content
df.write.mode("overwrite").option("header", "true").csv("download/employees_spark.csv")  # Save DataFrame as CSV, overwriting if it already exists

# Save Pandas DataFrame as Parquet file without including the index
print(df.toPandas())
df.toPandas().to_parquet("download/employees_pandas.parquet", index=False)