#!/bin/bash

# Ignorer complètement les migrations
export DJANGO_SKIP_MIGRATIONS=True

# Démarrer Django sans vérifier les migrations
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoApp.settings')
import django
django.setup()
from django.core.management import call_command
call_command('runserver', '0.0.0.0:8000', '--noreload', '--skip-checks')
"