# This notebook script demonstrates the pre-configured Spark session with Unity Catalog integration.
# It assumes that the Spark session is already available as `spark` in the global namespace.
# If connecting through VSCode, make sure you are connected to the existing Jupyter kernel available in port localhost:8888.

# The spark session should already be available
print(f"Spark version: {spark.version}")
print(f"Spark app name: {spark.sparkContext.appName}")
print(f"Default catalog: {spark.conf.get('spark.sql.defaultCatalog')}")

# List all schemas in the unity catalog
spark.sql("SHOW SCHEMAS IN unity").show()
# Show all tables in the default schema
spark.sql("SHOW TABLES IN unity.default").show()
# Create a new table in the default schema
spark.sql("""
CREATE OR REPLACE TABLE unity.default.employees (
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

spark.sql("SELECT * FROM unity.default.employees").show()
