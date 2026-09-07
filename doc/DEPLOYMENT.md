# Deployment Guide

## AI Payment Failure Recovery Agent

This document describes how to deploy the Django application using GitHub, Vercel, and Supabase PostgreSQL.

---

# 1. Deployment Architecture

```text
GitHub
   |
   v
Vercel
   |
   v
Django Application
   |
   v
Supabase PostgreSQL
```

---

# 2. Requirements

Before deployment, make sure you have:

* GitHub account
* Git installed
* Vercel account
* Supabase project
* Django project
* Production requirements file

---

# 3. Requirements File

The project uses a lightweight production requirements file.

```text
Django==5.2.17
gunicorn==23.0.0
whitenoise==6.12.0
dj-database-url==3.1.2
psycopg2-binary==2.9.12
numpy==2.2.6
scikit-learn==1.7.2
pandas==2.3.3
requests==2.34.2
```

---

# 4. GitHub

The source code is maintained in GitHub.

Repository:

```text
Payment-Failure-Recovery-Agent
```

Before deployment, verify:

* `requirements.txt` exists.
* `manage.py` exists.
* Django project package exists.
* `.gitignore` is configured.
* Secrets are not committed.
* Local database files are ignored.

---

# 5. Supabase Database

Create a PostgreSQL database using Supabase.

The application connects to the database using:

```env
DATABASE_URL=your-supabase-database-url
```

Do not publish the database URL.

---

# 6. Django Database Configuration

Django can use `dj-database-url` to read the database connection string.

Example configuration:

```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}
```

The exact configuration should match the project's current `settings.py`.

---

# 7. Environment Variables

Configure these variables in Vercel:

```text
SECRET_KEY
DEBUG
DATABASE_URL
```

Example:

```text
SECRET_KEY = production-secret-key
DEBUG = False
DATABASE_URL = PostgreSQL connection string
```

Never commit the actual values.

---

# 8. Vercel Configuration

The project uses `vercel.json` to configure deployment.

A suitable configuration is provided separately in this repository.

---

# 9. Static Files

Django static files are handled using WhiteNoise.

The production settings should include:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]
```

The project should also have appropriate static-file settings.

---

# 10. Deploying to Vercel

### Step 1

Push the project to GitHub.

```bash
git add .
git commit -m "Prepare project for deployment"
git push origin main
```

### Step 2

Open Vercel.

Create a new project and import the GitHub repository.

### Step 3

Configure environment variables.

Add:

```text
SECRET_KEY
DEBUG
DATABASE_URL
```

### Step 4

Deploy the project.

Vercel will build the application using the project configuration.

---

# 11. Database Migration

After connecting Vercel to Supabase, the production database must contain the Django tables.

Run migrations against the production database:

```bash
python manage.py migrate
```

Verify:

```bash
python manage.py showmigrations
```

---

# 12. Create Superuser

Create an administrator account using:

```bash
python manage.py createsuperuser
```

The administrator can access:

```text
/admin/
```

---

# 13. Verify Deployment

After deployment, test:

```text
/
```

Then test:

```text
/login/
```

```text
/signup/
```

```text
/dashboard/
```

```text
/make-payment/
```

```text
/recovery-dashboard/
```

```text
/audit-trail/
```

---

# 14. Common Deployment Problems

## UndefinedTable

Error:

```text
relation "auth_user" does not exist
```

Cause:

Django migrations have not been applied to the production database.

Solution:

```bash
python manage.py migrate
```

---

## Database Connection Error

Check:

* `DATABASE_URL`
* Supabase database availability
* PostgreSQL connection string
* SSL configuration
* Vercel environment variables

---

## ModuleNotFoundError

Check:

```bash
pip install -r requirements.txt
```

Make sure the required package is included in `requirements.txt`.

---

## Static File Problems

Check:

* WhiteNoise configuration
* `STATIC_URL`
* `STATIC_ROOT`
* `collectstatic` configuration
* Django production settings

---

# 15. Security Checklist

Before making the application public:

* [ ] `DEBUG=False`
* [ ] Secret key stored in environment variables
* [ ] Database URL stored in environment variables
* [ ] Database password not in GitHub
* [ ] `.env` ignored
* [ ] `db.sqlite3` ignored
* [ ] CSRF protection enabled
* [ ] Admin access protected
* [ ] Production database configured
* [ ] Sensitive logs removed

---

# 16. Production Architecture

```text
                       INTERNET
                           |
                           v
                    +-------------+
                    |   Vercel    |
                    +-------------+
                           |
                           v
                    +-------------+
                    |   Django    |
                    | Application |
                    +-------------+
                           |
                           | DATABASE_URL
                           v
                    +-------------+
                    |  Supabase   |
                    | PostgreSQL  |
                    +-------------+
```

---

# 17. Deployment Summary

The final deployment pipeline is:

```text
Developer
    |
    v
Git
    |
    v
GitHub
    |
    v
Vercel
    |
    v
Django
    |
    v
Supabase PostgreSQL
```

This provides a clean separation between source-code hosting, application deployment, and database hosting.

```
```
