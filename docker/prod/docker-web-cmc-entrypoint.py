#!/usr/bin/python3
import os
import django

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Установите переменную окружения DJANGO_SETTINGS_MODULE, чтобы указать на файл настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")

# Загрузите настройки Django
django.setup()


import subprocess
from django.core.management import call_command
from django.core.management.base import CommandError

from cmc.models import Cryptocurrency
from blockchain.models import Blockchain
from exchanger.models import Exchanger


def run_command(command, success_message, failure_message):
    try:
        subprocess.check_call(command, shell=True)
        print(success_message)
    except subprocess.CalledProcessError:
        print(failure_message)


def load_fixture(model_name, fixture_path):
    try:
        call_command('loaddata', fixture_path)
        print(f"Successfully loaded data from {model_name}")
    except CommandError as e:
        print(f"Failed to load data from {model_name}: {e}")


def check_database_data(model, fixture_path):
    if model.objects.exists():
        print(f"Data exists in the {model._meta.verbose_name_plural.title()} model.")
    else:
        load_fixture(model._meta.verbose_name_plural.title(), fixture_path)


def main():
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Successful collectstatic", "Not successful collectstatic")

    # Apply database makemigrations
    run_command("python manage.py makemigrations", "Successful makemigrations", "Not successful makemigrations")

    # Apply database migrations
    run_command("python manage.py migrate", "Successful migrate", "Not successful migrate")

    # Check database data and load fixtures
    check_database_data(Cryptocurrency, "../../data/fixtures/cryptocurrency.json")
    check_database_data(Blockchain, "../../data/fixtures/blockchain.json")
    check_database_data(Exchanger, "../../data/fixtures/exchanger.json")

    # Apply create superuser. Name, Email and password set in ".env"
    run_command("python manage.py createsuperuser --noinput", "Successful created superuser", "Not created superuser")

    # Start server
    print("Starting server")
    subprocess.call("gunicorn core.wsgi:application --bind 0.0.0.0:8000", shell=True)


if __name__ == "__main__":
    main()
