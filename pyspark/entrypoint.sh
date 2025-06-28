#!/bin/bash

# Entrypoint script for PySpark with Unity Catalog
# This script sets up IPython startup scripts and starts Jupyter Lab

set -e

echo "🔧 Setting up IPython startup scripts..."

# Create IPython profile directory if it doesn't exist
IPYTHON_DIR="${HOME}/.ipython/profile_default/startup"
mkdir -p "${IPYTHON_DIR}"

# Copy the startup script to IPython startup directory
cp /opt/startup_spark.py "${IPYTHON_DIR}/00-spark-unity-catalog.py"

echo "📝 IPython startup script installed at: ${IPYTHON_DIR}/00-spark-unity-catalog.py"

# Create a custom Jupyter configuration to ensure proper kernel setup
JUPYTER_CONFIG_DIR="${HOME}/.jupyter"
mkdir -p "${JUPYTER_CONFIG_DIR}"

cat > "${JUPYTER_CONFIG_DIR}/jupyter_notebook_config.py" << 'EOF'
# Jupyter configuration for Unity Catalog setup
c = get_config()

# Ensure IPython startup scripts are executed
c.IPKernelApp.exec_lines = [
    'print("🔄 Loading Unity Catalog Spark session...")'
]

# Set environment variables for better Spark integration
import os
os.environ['PYSPARK_DRIVER_PYTHON'] = 'jupyter'
os.environ['PYSPARK_DRIVER_PYTHON_OPTS'] = 'lab'
EOF

echo "📋 Jupyter configuration created"

# Print helpful information
echo ""
echo "🎯 Starting Jupyter Lab with Unity Catalog integration..."
echo "📖 The 'spark' object will be automatically available in all notebooks"
echo "🌐 Unity Catalog server: http://server:8080"
echo "📊 Spark UI will be available at: http://localhost:4040"
echo ""

# Execute the original command
exec "$@"
