# PowerShell script to automate release of ipynbcleaner

# Abort on any error
$ErrorActionPreference = 'Stop'

Write-Host "Running tests..."
python -m unittest discover -s tests

Write-Host "Building package..."
python -m build

Write-Host "Checking distribution with twine..."
 twine check dist/*

$uploadTest = Read-Host "Upload to TestPyPI now? (y/n)"
if ($uploadTest -eq 'y') {
    Write-Host "Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
} else {
    Write-Host "Skipping TestPyPI upload."
}

$uploadProd = Read-Host "Upload to PyPI (official) now? (y/n)"
if ($uploadProd -eq 'y') {
    Write-Host "Uploading to PyPI..."
    twine upload dist/*
} else {
    Write-Host "Release script finished without publishing to PyPI."
}
