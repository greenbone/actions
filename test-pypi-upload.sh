#!/bin/bash

# Test script for pypi-upload action
# This simulates the workflow steps to verify they work correctly

set -e  # Exit on any error

echo "🧪 Testing PyPI Upload Action Workflow"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}📋 Step: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to test a command
test_command() {
    local cmd="$1"
    local description="$2"
    
    print_step "$description"
    echo "Running: $cmd"
    
    if eval "$cmd"; then
        print_success "$description completed successfully"
        return 0
    else
        print_error "$description failed"
        return 1
    fi
}

# Test if we're in a directory with a Python project
if [ ! -f "pyproject.toml" ]; then
    print_warning "No pyproject.toml found in current directory"
    echo "This test should be run in a Python project directory with pyproject.toml"
    echo ""
    echo "To test properly:"
    echo "1. cd to a Python project directory (like greenbone-feed-sync)"
    echo "2. Run this script from there"
    echo ""
    echo "For now, testing the individual commands..."
    echo ""
fi

# Step 1: Install pip and poetry (simulate what the action does)
print_step "Installing/upgrading pip and poetry"
test_command "python3 -m pip install --upgrade pip" "Upgrade pip"
test_command "python3 -m pip install --upgrade poetry" "Install/upgrade poetry"

echo ""

# Step 2: Check poetry configuration (if pyproject.toml exists)
if [ -f "pyproject.toml" ]; then
    test_command "poetry check" "Check poetry configuration"
else
    print_warning "Skipping poetry check - no pyproject.toml found"
fi

echo ""

# Step 3: Install dependencies (if pyproject.toml exists)
if [ -f "pyproject.toml" ]; then
    test_command "poetry install" "Install dependencies"
else
    print_warning "Skipping poetry install - no pyproject.toml found"
fi

echo ""

# Step 4: Build (if pyproject.toml exists)
if [ -f "pyproject.toml" ]; then
    test_command "poetry build" "Build package"
else
    print_warning "Skipping poetry build - no pyproject.toml found"
fi

echo ""

# Step 5: Verify package metadata (if dist/ exists)
if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
    test_command "python3 -m pip install --upgrade twine" "Install twine"
    test_command "python3 -m twine check dist/*" "Verify package metadata"
else
    print_warning "Skipping twine check - no dist/ directory with files found"
fi

echo ""
echo "🎉 Test completed!"
echo ""
echo "📝 Summary:"
echo "- This script tests the individual commands from the pypi-upload action"
echo "- Run this in a Python project directory for full testing"
echo "- All commands should pass before submitting the PR"
echo ""
echo "🚀 To test with a real project:"
echo "1. Clone the greenbone-feed-sync repo"
echo "2. cd into that directory"
echo "3. Run this script: bash /path/to/test-pypi-upload.sh"