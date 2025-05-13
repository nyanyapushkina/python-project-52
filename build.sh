#!/bin/bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate