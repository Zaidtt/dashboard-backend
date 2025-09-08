#!/usr/bin/env bash
# build.sh
set -o errexit  # aborta en errores

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

