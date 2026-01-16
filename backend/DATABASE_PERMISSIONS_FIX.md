# Database Permissions Fix

## Problem
**Error**: "attempt to write a readonly database"

**Cause**: SQLite database file (`db.sqlite3`) doesn't have write permissions on Elastic Beanstalk EC2 instance.

## Solution Applied

### 1. Created `.ebextensions/06_fix_db_permissions.config`
This ensures database permissions are fixed during deployment.

### 2. Updated `.platform/hooks/postdeploy/01_migrate.sh`
Added permission fixing commands after migrations run:
- Set database file permissions: `chmod 664`
- Set directory permissions: `chmod 775`
- Change ownership to `webapp:webapp` user

## What Was Fixed

1. ✅ Database file (`db.sqlite3`) now has write permissions (664)
2. ✅ Directory (`/var/app/current`) is writable (775)
3. ✅ Ownership set to `webapp` user (runs Django app)

## Testing

After deployment, try signing up again. The error should be resolved.

## If Issue Persists

If you still get the error, we can:

1. **Move database to writable location** (e.g., `/tmp` or `/var/app/current/data/`)
2. **Use PostgreSQL/RDS** instead of SQLite (recommended for production)
3. **Check actual user permissions** via SSH: `eb ssh` then `ls -la /var/app/current/db.sqlite3`

## Alternative: Use RDS PostgreSQL (Production)

For production, SQLite is not recommended. Consider using RDS PostgreSQL:

1. Create RDS PostgreSQL instance in AWS Console
2. Update `settings.py` to use PostgreSQL
3. Set environment variables for database credentials

See `ELASTIC_BEANSTALK_DEPLOYMENT.md` for RDS setup instructions.
