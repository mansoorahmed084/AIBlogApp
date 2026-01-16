#!/bin/bash
# Run migrations after deployment
source /var/app/venv/*/bin/activate
cd /var/app/current

# Ensure directory is writable before migrations
chmod 775 /var/app/current || true

# Run migrations (this creates db.sqlite3 if it doesn't exist)
python manage.py migrate --noinput

# Fix database file permissions after migrations (SQLite needs write access)
if [ -f /var/app/current/db.sqlite3 ]; then
    chmod 664 /var/app/current/db.sqlite3 || true
    # Try to set ownership to webapp user (may fail if already correct)
    chown webapp:webapp /var/app/current/db.sqlite3 2>/dev/null || true
fi
# Ensure the directory ownership
chown webapp:webapp /var/app/current 2>/dev/null || true
