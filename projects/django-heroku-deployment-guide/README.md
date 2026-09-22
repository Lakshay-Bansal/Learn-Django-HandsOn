# 🚀 Django Deployment on Heroku: Complete Hands-On Guide

This project is a complete reference and working template demonstrating how to configure and deploy a **Django** web application to the **Heroku** cloud platform.

---

## 📑 Table of Contents
1. [Why Heroku Needs Special Configuration](#-why-heroku-needs-special-configuration)
2. [Required Files & What Needs to be Updated](#-required-files--what-needs-to-be-updated)
   - [1. Procfile](#1-procfile)
   - [2. runtime.txt](#2-runtimetxt)
   - [3. requirements.txt](#3-requirementstxt)
   - [4. depDjangoHeroku/settings.py](#4-depdjangoherokusettingspy)
   - [5. .env.example & Environment Variables](#5-envexample--environment-variables)
   - [6. .gitignore](#6-gitignore)
3. [Step-by-Step Deployment Walkthrough](#-step-by-step-deployment-walkthrough)
4. [Deploying as a Subtree from a Monorepo](#-deploying-as-a-subtree-from-a-monorepo)
5. [Common Heroku Errors & How to Fix Them](#-common-heroku-errors--how-to-fix-them)

---

## 💡 Why Heroku Needs Special Configuration

Heroku operates on the **Twelve-Factor App** methodology and utilizes containerized execution units called **Dynos**:

1. **Stateless Dynos**: The local filesystem on a Heroku dyno is **ephemeral**. Any files saved locally (such as SQLite databases or user-uploaded media) are wiped whenever a dyno sleeps, restarts, or deploys new code.
2. **Environment Variables**: Production credentials (`SECRET_KEY`, `DATABASE_URL`, API keys) must be injected via Heroku Config Vars rather than hardcoded in files.
3. **Dedicated WSGI Server**: Django’s built-in `python manage.py runserver` is strictly for local development and is single-threaded. Heroku requires a production-grade WSGI server like **Gunicorn**.
4. **Static Files Serving**: In production, Django does not serve static assets (`CSS`, `JS`, images) by default. **WhiteNoise** is required to compress and serve static files directly through Gunicorn without needing an external Nginx server.

---

## 🛠 Required Files & What Needs to be Updated

Here is the exact checklist of files required for Heroku deployment:

```
projects/django-heroku-deployment-guide/
├── Procfile                     # <-- Tells Heroku how to run your application
├── runtime.txt                  # <-- Tells Heroku which Python version to install
├── requirements.txt             # <-- Dependencies (Gunicorn, psycopg2, whitenoise, etc.)
├── .env.example                 # <-- Template of environment variables
├── .gitignore                   # <-- Prevents uploading secrets & cache files
└── depDjangoHeroku/
    ├── settings.py              # <-- Updated settings for database, staticfiles, & security
    └── wsgi.py                  # <-- WSGI entrypoint for Gunicorn
```

---

### 1. `Procfile`

The `Procfile` must be located in the root directory of your app (no file extension, capital `P`).

```procfile
web: gunicorn depDjangoHeroku.wsgi --log-file -
```

#### What this does:
- **`web:`**: Declares the process type as a web dyno capable of receiving HTTP traffic.
- **`gunicorn depDjangoHeroku.wsgi`**: Starts Gunicorn targeting your project's `wsgi.py` entrypoint.
  > **Note**: If your project folder is named differently (e.g., `myproject`), change `depDjangoHeroku.wsgi` to `myproject.wsgi`.
- **`--log-file -`**: Routes Gunicorn access and error logs to standard output (`stdout`), allowing you to view live logs using `heroku logs --tail`.

#### Optional (Automatic Migrations):
To automatically run database migrations on every deploy:
```procfile
release: python manage.py migrate
web: gunicorn depDjangoHeroku.wsgi --log-file -
```

---

### 2. `runtime.txt`

Specifies the exact Python version that the Heroku Python buildpack will install.

```text
python-3.8.8
```

> ⚠️ **IMPORTANT RULE**:
> `runtime.txt` must contain **only** the runtime string (e.g. `python-3.8.8`, `python-3.10.13`, `python-3.11.7`).
> **Do NOT add comments, spaces, or extra lines** in `runtime.txt`, or Heroku buildpack will fail with `Requested runtime is not available`.

---

### 3. `requirements.txt`

In addition to `Django`, Heroku requires specific packages:

| Package | Purpose for Heroku |
| :--- | :--- |
| `gunicorn` | Production WSGI HTTP server |
| `dj-database-url` | Parses Heroku's dynamic `DATABASE_URL` environment variable into Django's `DATABASES` dictionary |
| `psycopg2` or `psycopg2-binary` | PostgreSQL database adapter for Python |
| `whitenoise` | Serves and compresses static files directly from Gunicorn without Nginx |
| `python-decouple` | Strictly decouples secret keys and environment variables from source code |
| `django-heroku` | Heroku's helper library for automated database, logging, and static asset wiring |

---

### 4. `depDjangoHeroku/settings.py`

Modify `settings.py` to adapt between local development and Heroku production:

#### A. Decouple Secrets & Settings
```python
from decouple import config

# Fetch from .env locally or Heroku Config Vars in production
SECRET_KEY = config('SECRET_KEY', default='local-insecure-dev-key')
DEBUG = config('DEBUG', cast=bool, default=True)

# Allow Heroku domain and localhost
ALLOWED_HOSTS = [
    host.strip()
    for host in config('ALLOWED_HOST', default='localhost,127.0.0.1').split(',')
    if host.strip()
]
```

#### B. Configure WhiteNoise Middleware
Place `WhiteNoiseMiddleware` immediately following `SecurityMiddleware`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Add here!
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

#### C. Database Switching (SQLite locally vs PostgreSQL on Heroku)
Heroku injects a `DATABASE_URL` config variable when you attach Heroku Postgres:
```python
import dj_database_url

database_url = config('DATABASE_URL', default='')

if DEBUG and not database_url:
    # Local development with SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Heroku production with PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            ssl_require=True
        )
    }
```

#### D. Static Files & WhiteNoise Storage
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### E. Heroku Helper Integration
At the very end of `settings.py`:
```python
import django_heroku
django_heroku.settings(locals())
```

---

### 5. `.env.example` & Environment Variables

Never commit real `.env` files with production secret keys to Git. Create a `.env.example` file as a safe reference template showing which variables are needed:

```env
SECRET_KEY=django-insecure-local-dev-secret-key-change-in-production
DEBUG=True
ALLOWED_HOST=127.0.0.1,localhost
```

#### 🔐 Deep Dive: What is `SECRET_KEY` and Why is it Critical?

Django's **`SECRET_KEY`** is a cryptographic salt used across the framework for security operations:

* **Session Security**: Django signs session cookies with this key. If an attacker knows your production `SECRET_KEY`, they can forge valid session cookies for any user—including superusers—and bypass login authentication entirely.
* **CSRF Protection**: Secures Cross-Site Request Forgery tokens to ensure form submissions come from legitimate users.
* **Password Reset Links**: Django signs temporary password reset tokens with this key. A compromised key allows attackers to craft valid reset tokens and hijack accounts.
* **Message & Cookie Signing**: Any data signed with `django.core.signing` relies on this key for tamper prevention.

> ⚠️ **Why the dummy key in `.env.example`?**
> - For **local development** on your machine (`127.0.0.1`), a dummy string like `django-insecure-local-dev-secret-key-change-in-production` is safe because no real users or production data exist locally.
> - For **production on Heroku**, you must **NEVER** use the default key or commit your real key to Git. Instead, generate a unique cryptographically strong random key and inject it directly into Heroku's encrypted Config Vars.

#### How to Generate and Set a Strong Production `SECRET_KEY`:
```bash
# 1. Generate a 50-character cryptographically secure key:
python -c "import secrets; print(secrets.token_urlsafe(50))"

# 2. Set it on Heroku (or pass the generation command directly):
heroku config:set SECRET_KEY='your-generated-secure-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOST='your-app-name.herokuapp.com'
```

---

### 6. `.gitignore`

Ensure your `.gitignore` contains:
```gitignore
.env
env/
venv/
__pycache__/
*.py[cod]
staticfiles/
db.sqlite3
```

---

## 🚀 Step-by-Step Deployment Walkthrough

### Step 1: Install & Login to Heroku CLI
```bash
# Verify Heroku CLI is installed
heroku --version

# Log in to your Heroku account
heroku login
```

### Step 2: Create Heroku Application
```bash
# Create a new app (replace with your desired app name)
heroku create my-django-app-demo
```

### Step 3: Add PostgreSQL Database Add-on
```bash
# Attach Heroku Postgres (essential tier)
heroku addons:create heroku-postgresql:essential-0
```
> Heroku will automatically add the `DATABASE_URL` config variable to your app.

### Step 4: Set Production Config Vars
```bash
heroku config:set SECRET_KEY='strong-production-random-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOST='my-django-app-demo.herokuapp.com'
```

### Step 5: Deploy the Code
If working directly from a dedicated repository:
```bash
git add .
git commit -m "Configure Django for Heroku deployment"
git push heroku main
```

### Step 6: Run Database Migrations on Heroku
```bash
heroku run python manage.py migrate
```

### Step 7: Create an Admin Superuser
```bash
heroku run python manage.py createsuperuser
```

### Step 8: Open the Live Application & View Logs
```bash
# Open application in browser
heroku open

# View live streaming logs
heroku logs --tail
```

---

## 📦 Deploying as a Subtree from a Monorepo

Because this guide lives inside a subdirectory (`projects/django-heroku-deployment-guide`), you can deploy just this directory to Heroku without pushing the entire root repo:

```bash
# Add the Heroku git remote
heroku git:remote -a my-django-app-demo

# Push only the subfolder to Heroku's main branch
git subtree push --prefix=projects/django-heroku-deployment-guide heroku main
```

---

## 🩺 Common Heroku Errors & How to Fix Them

### 1. `H10 - App Crashed`
- **Cause**: Gunicorn failed to boot or `Procfile` had a syntax error.
- **Fix**: Check `heroku logs --tail`. Ensure the project name in `Procfile` matches your directory containing `wsgi.py`.

### 2. `H14 - No web processes running`
- **Cause**: The dyno is scaled to 0.
- **Fix**: Run `heroku ps:scale web=1`.

### 3. `Collectstatic Error during build`
- **Cause**: Missing `STATIC_ROOT` in `settings.py` or invalid static file reference.
- **Fix**: Verify `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`. Alternatively, temporarily disable collectstatic to diagnose:
  ```bash
  heroku config:set DISABLE_COLLECTSTATIC=1
  ```

### 4. `DisallowedHost: Invalid HTTP_HOST header`
- **Cause**: The Heroku app URL is not in `ALLOWED_HOSTS`.
- **Fix**: Update the config var:
  ```bash
  heroku config:set ALLOWED_HOST='your-app-name.herokuapp.com'
  ```

---

## 📚 References
- [Heroku Dev Center: Deploying Python and Django Applications](https://devcenter.heroku.com/articles/deploying-python)
- [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/)
- [Twelve-Factor App Principles](https://12factor.net/)
