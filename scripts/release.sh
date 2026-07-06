#!/usr/bin/env bash

# exit on any error
set -e

# 1️⃣ Run tests
echo "Running tests..."
python -m unittest discover -s tests

# 2️⃣ Build distribution
echo "Building package..."
python -m build

# 3️⃣ Verify artifacts
echo "Checking distribution with twine..."
 twine check dist/*

# 4️⃣ Upload to TestPyPI
read -p "Upload to TestPyPI now? (y/n) " upload_test
if [[ "$upload_test" == "y" ]]; then
  echo "Uploading to TestPyPI..."
  twine upload --repository testpypi dist/*
else
  echo "Skipping TestPyPI upload."
fi

# 5️⃣ Confirm upload to real PyPI
read -p "Upload to PyPI (official) now? (y/n) " upload_prod
if [[ "$upload_prod" == "y" ]]; then
  echo "Uploading to PyPI..."
  twine upload dist/*
else
  echo "Release script finished without publishing to PyPI."
fi
