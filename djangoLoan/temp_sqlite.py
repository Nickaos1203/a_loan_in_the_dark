#!/usr/bin/env python
import re

with open('djangoApp/settings.py', 'r') as f:
    content = f.read()

sqlite_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Commented out SQL Server config for future reference
# '''

pattern = r'DATABASES\s*=\s*\{.*?\}\s*\}'
new_content = re.sub(pattern, sqlite_config, content, flags=re.DOTALL)

with open('djangoApp/settings.py', 'w') as f:
    f.write(new_content)

print("Configuration temporaire mise à jour pour utiliser SQLite")
