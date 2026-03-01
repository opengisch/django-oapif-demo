#!/usr/bin/env bash

set -Eeuo pipefail

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py generate_qgis_project

exec "$@"
