#!/bin/bash
#
# Setup script for OpenCode Skills MCP Server
#

set -e

echo "========================================"
echo "OpenCode Skills MCP Server Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "Error: Python 3.9 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python version: $PYTHON_VERSION"
echo ""

# Create logs directory
echo "Creating logs directory..."
mkdir -p logs
echo "✓ Created logs directory"
echo ""

# Install dependencies
echo "Installing dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -e .
elif command -v uv &> /dev/null; then
    uv pip install -e .
elif command -v pip &> /dev/null; then
    pip install -e .
else
    echo "Error: No package manager found (pip, pip3, or uv)"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Run validation
echo "Running quick validation..."
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from opencode_skills_mcp import create_server
    print('✓ MCP server imports successfully')
except Exception as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Setup Complete!"
    echo "========================================"
    echo ""
    echo "Next steps:"
    echo "1. Add server to OpenCode config (see README.md)"
    echo "2. Restart OpenCode"
    echo ""
    echo "Server entry point: src/opencode_skills_mcp/server.py"
    echo "Logs: logs/opencode_skills_mcp.log"
else
    echo ""
    echo "Setup failed. Check error messages above."
    exit 1
fi
