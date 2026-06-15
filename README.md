# OE Inventory

Web application for managing the IT inventory (devices, mobile lines, licenses,
access cards, staff, etc.). Built with Django and a MySQL/MariaDB backend; it is a
web port of a former Tkinter desktop application.

## Tech stack

- **Python** 3.10+
- **Django** 4.1
- **MySQL / MariaDB** (via [PyMySQL](https://pypi.org/project/PyMySQL/), installed as
  `MySQLdb` in `src/oe_inventory/__init__.py`)
- **openpyxl** for Excel export, **reportlab** for the staff inventory PDF
- **Bootstrap 5** + **DataTables** + **SweetAlert2** on the front end (loaded via CDN)

## Project layout

```
oe_inventory_py_web/
├── requirements.txt
├── README.md
└── src/                       # Django project root (contains manage.py)
    ├── manage.py
    ├── .env                   # local secrets — NOT committed
    ├── .env.example           # template for .env
    ├── oe_inventory/          # settings, urls, wsgi/asgi
    └── oe_inventory_py_web/   # the application (models, views, templates, static)
```

## Setup

From the repository root:

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp src/.env.example src/.env
#    then edit src/.env with your real values (see below)

# 4. Apply migrations and run the development server
cd src
python manage.py migrate
python manage.py runserver
```

The app is then available at <http://127.0.0.1:8000/> (login at `/login/`).

## Environment variables

Configuration is read from `src/.env` (loaded automatically by
`settings.py`). See `src/.env.example` for the full list:

| Variable                | Description                                  | Default                  |
| ----------------------- | -------------------------------------------- | ------------------------ |
| `DJANGO_SECRET_KEY`     | Django secret key (**required**)             | —                        |
| `DJANGO_DEBUG`          | `True` / `False`                             | `False`                  |
| `DJANGO_ALLOWED_HOSTS`  | Comma-separated host list                    | `localhost,127.0.0.1`    |
| `DB_NAME`               | Database name                                | `oees_inventory`         |
| `DB_USER`               | Database user (**required**)                 | —                        |
| `DB_PASSWORD`           | Database password (**required**)             | —                        |
| `DB_HOST`               | Database host                                | `localhost`              |
| `DB_PORT`               | Database port                                | `3306`                   |
| `DJANGO_LOG_LEVEL`      | Log level (DEBUG/INFO/WARNING/ERROR)         | `INFO`                   |

Generate a fresh secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> **Security:** never commit `src/.env`. It is already listed in `.gitignore`.
> Rotate any secret that was previously committed to version control.

## Running tests

```bash
cd src
python manage.py test
```

The test suite runs against an in-memory SQLite database (configured automatically
in `settings.py` when `test` is in the command), so it does **not** require a
running MySQL server.

## Staff screen

- Uploaded staff documents are stored under `MEDIA_ROOT/staff_docs/<staff_id>/`.
- The inventory PDF report uses an optional logo at
  `oe_inventory_py_web/static/images/report_logo.png` (it is omitted if missing).
- Emailing the report requires the `EMAIL_*` and `STAFF_REPORT_RECIPIENT` variables
  (see `.env.example`). The Tkinter version had Gmail credentials hardcoded — those
  must be **revoked** and configured via the environment instead.

## Database notes

The models map to a pre-existing legacy schema (`managed = True`, tables prefixed
`oees_`). Authentication uses a custom user model
(`oe_inventory_py_web.CustomUser`) that extends Django's `AbstractUser` with the
application's permission flags.
