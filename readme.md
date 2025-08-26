# Blog Project — Minimal Django Blog

> **Short description**: A simple blog/magazine web application built with Django. It includes a homepage with featured posts, categorization, search, post detail pages with comments, a contact form (sends email), admin management, and a set of static templates and assets for a minimal magazine layout.

---

## Table of contents

- [Project overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Quick installation (development)](#quick-installation-development)
- [Configuration](#configuration)
- [Usage / Available routes](#usage--available-routes)
- [Examples](#examples)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [Security & sensitive data](#security--sensitive-data)
- [License](#license)
- [Notes & known issues](#notes--known-issues)

---

## Project overview

This repository contains a Django-based blog application (project directory: `blog_project`) with templates, static assets, and a small app called `blog_app`. The UI is a minimal magazine-style theme (templates under `templates/`) and the project includes example/static data (a `db.sqlite3` file is present in the repo).

The app supports:

- Posts (publish/draft)
- Categories
- Post detail pages with view counters
- Nested comments (comment replies)
- A contact form which is wired to send email
- Simple notices/announcement model
- Search functionality
- Django admin for managing posts, categories, and comments

> Note: Some Python files in the provided archive appear to include placeholder lines (`...`) in places. I documented what I could inspect; please review the files `blog_app/models.py` and `blog_app/views.py` in your working copy to ensure no code is missing or intentionally redacted.

---

## Features

- Homepage with a featured/main post (flag `Main_post` used in templates)
- Post list and single post detail pages
- Category pages to filter posts by category
- Comment submission (`<post_id>/add_comment/` route)
- Search: `/search/?q=your+query`
- Contact page with email sending
- Admin site for CRUD on posts/categories/comments
- Static assets (CSS, JS, images, fonts) included in `static/`

---

## Requirements

- Python 3.10+ (project was packaged with a Python 3.11 environment, but Django 5.x supports Python 3.10/3.11+)
- `pip` and virtual environment tooling
- For production: PostgreSQL is referenced in `settings.py` (but a `db.sqlite3` file is included for demo)
- See `requirements.txt` for full Python package list. Key packages include:
  - Django==5.2.4
  - djangorestframework
  - Pillow
  - psycopg2 or PyMySQL (drivers in `requirements.txt`)

---

## Quick installation (development)

> These steps assume you are on macOS / Linux. On Windows, adapt `source venv/bin/activate` to `venv\\Scripts\\activate`.

1. Unzip / clone the project and `cd` into the project folder that contains `manage.py` (e.g. `blog_project/`).

```bash
# create virtual environment
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

2. If you prefer to use the included demo SQLite database, no DB setup is required. If you want to use PostgreSQL (recommended for production), create the DB and update `DATABASES` in `blog_project/settings.py` or set environment variables according to your preferred configuration.

3. Apply migrations (if you are not using the provided `db.sqlite3` or you changed DB):

```bash
python manage.py migrate
```

4. Create a superuser to access Django admin:

```bash
python manage.py createsuperuser
```

5. (Optional) Collect static assets for production:

```bash
python manage.py collectstatic
```

6. Run the development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

---

## Configuration

Important settings live in `blog_project/settings.py`. Before deploying to production, make the following changes:

- **SECRET_KEY**: Do not keep the secret key in source control. Use an environment variable or a secrets manager and load it in `settings.py`.
- **DEBUG**: Set `DEBUG = False` for production.
- **ALLOWED_HOSTS**: Add your domain(s) to `ALLOWED_HOSTS`.
- **Database**: The sample settings reference PostgreSQL. Either configure PostgreSQL credentials or use the included `db.sqlite3` as a local demo database. Example env variables you might use:

```bash
export DJANGO_SECRET_KEY="your-secret-key"
export DJANGO_DEBUG=False
export DATABASE_NAME=blog_db
export DATABASE_USER=postgres
export DATABASE_PASSWORD=secure-password
export DATABASE_HOST=127.0.0.1
export DATABASE_PORT=5432
```

- **Email**: The contact form uses Django's SMTP email backend. Configure `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and related settings through environment variables. Do not commit credentials to the repository.

- **Static & media files**: `STATIC_URL`, `MEDIA_URL` and `MEDIA_ROOT` are configured in `settings.py` — ensure `MEDIA_ROOT` is writable by your web server.

---

## Usage / Available routes

Routes available in the current app (based on `blog_app/urls.py` and templates):

- `/` — Home page (featured posts + latest posts)
- `/about/` — About page
- `/contact/` — Contact form
- `/search/?q=term` — Search results for `term`
- `/<int:pk>/` — Blog post detail page (example: `/12/`)
- `/category/<int:pk>/` — List posts in category
- `/<int:pk>/add_comment/` — POST endpoint to submit a comment for post with id `pk`
- `/admin/` — Django admin site (requires superuser)

---

## Examples

> The exact model fields were partially redacted in the distributed copy. The examples below assume commonly used field names (`title`, `content`, `category`, `status`, `Main_post`). If your models use different names, adapt accordingly.

Create a category and a post from Django shell:

```python
# run: python manage.py shell
from blog_app.models import Category, Blog
cat = Category.objects.create(name='Tech')
post = Blog.objects.create(title='My First Post', content='Hello world', status='1', category=cat, Main_post=True)
```

Search example (browser URL):

```
http://127.0.0.1:8000/search/?q=django
```

Submit a comment (HTML form on a post detail page): the form posts to `/<post_id>/add_comment/` and typically includes `name`, `email`, `message`, and optional `parent` if a reply.

---

## Project structure (key files & folders)

```
blog_project/                 # Django project root
├─ blog_app/                  # Main app (models, views, urls, admin)
├─ templates/                 # HTML templates (base, home, blog_detail, contact...)
├─ static/                    # CSS, JS, images, fonts
├─ db.sqlite3                  # Example/demo database (optional)
├─ manage.py
├─ requirements.txt
└─ blog_project/settings.py
```

> Note: This repository also contains a `blogenv/` directory (a virtual environment) and a `.git/` directory. It is a best practice **not** to commit virtual environments or other generated binary artifacts. Consider removing `blogenv/` from the repo and adding it to `.gitignore`.

---

## Contributing

If you plan to accept contributions, consider adding a `CONTRIBUTING.md` with contribution steps. A suggested minimal workflow:

1. Fork the repository and create a feature branch: `git checkout -b feature/my-change`
2. Make the change, run migrations and tests (if added)
3. Open a Pull Request with a clear description of the change
4. Ensure secrets are not committed

Suggested code-style checks:

- Use `flake8` or `black` for style formatting
- Add unit tests for views/models where appropriate

---

## Security & sensitive data

**Important:** `settings.py` in this archive contains hard-coded sensitive data (SECRET_KEY and SMTP credentials). This is a security risk. Do not publish those credentials or push them to a public repository. Steps to remediate:

- Move secrets into environment variables (use `os.environ.get(...)`) or use a secrets manager.
- Remove sensitive values from git history if they were previously committed (tools: `git filter-repo`, `bfg-repo-cleaner`).
- Remove the `blogenv/` virtualenv from the repo and add `venv/` or similar to `.gitignore`.

---

## License

No license file was included in the repository. Without an explicit license, the project is effectively "All rights reserved". If you intend to open-source this project, add a license (for example MIT, Apache-2.0, or GPL) by adding a `LICENSE` file.

---

## Notes & known issues

- Some Python files contain placeholder lines (literal `...`) which suggest parts of the implementation may be missing or were redacted. Please inspect and restore full implementations in `blog_app/models.py` and `blog_app/views.py` where necessary.
- The repo contains `db.sqlite3` — if you will use another DB (Postgres), update `settings.py` accordingly and re-run migrations.
- Before deploying to production, update security-related settings and verify email/sendmail configuration.

---

If you want, I can also:

- Prepare a `.env.example` and show how to load secrets safely
- Create a `Procfile` / simple deployment guide for Gunicorn + Nginx or for a PaaS (Heroku-like)
- Produce a `Dockerfile` and `docker-compose.yml` for local development

Let me know which of the above you prefer and I will add it to the README or create the supporting files.

