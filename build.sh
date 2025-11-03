#!/bin/bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Optional: Collect static files if needed
# python manage.py collectstatic --noinput

echo "Build completed successfully!"
