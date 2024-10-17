
# Beam

## Overview
Brief description of the project.

## Prerequisites
- Docker
- Docker Compose
- Python 3.10 (or higher)
- Poetry
- PostgreSQL
- Redis
- Postgis extension for PostgreSQL
- Celery

## Getting Started
1. Clone the repository, set .env variables and navigate to the project directory, run this commands on different terminal windows to start celery and redis server:

```bash
redis-server
```

```bash
python3 -m celery -A beam worker --loglevel=INFO
```

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Set up the database and install Postgis extension for PostgreSQL:
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE beam;
CREATE USER beam_user WITH PASSWORD 'admin123';
ALTER ROLE beam_user SET client_encoding TO 'utf8';
ALTER ROLE beam_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE beam_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE beam TO beam_user; 
CREATE EXTENSION IF NOT EXISTS postgis;
```

3. in the manage.py file, set the values ``​​DJANGO_SETTINGS_MODULE``, ``beam.settings.local`` or development to select the launch, later you will need to put a choice there via .env:
```bash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beam.settings.base")
```

4. To run the project manually use the following command:
```bash
poetry run python3 manage.py migrate && poetry run python3 manage.py runserver
```

5. To run the project with Docker use the following command:

    1. Go to the entrypoints directory
        ```bash
        cd entrypoints/
        ```
    2. Don't forget to grant execution rights to the run_docker.sh script if necessary:
        ```bash
        chmod +x run_docker.sh
        ```
    3. Run the script run_docker.sh:
        ```bash
        ./run_docker.sh
        ```