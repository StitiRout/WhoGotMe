from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection

from core.models import Breach


def _table_exists(name: str) -> bool:
    return name in connection.introspection.table_names()

# Rows from backend/thedb.sql
BREACH_ROWS = [
    {
        "email": "john@gmail.com",
        "breach_name": "LinkedIn",
        "breach_date": date(2021, 4, 15),
        "data_exposed": "Email, Password",
        "severity": "High",
        "description": "Professional networking platform data breach.",
    },
    {
        "email": "john@yahoo.com",
        "breach_name": "Facebook",
        "breach_date": date(2020, 11, 2),
        "data_exposed": "Phone Number, Email",
        "severity": "High",
        "description": "Large social media platform breach.",
    },
    {
        "email": "alice@gmail.com",
        "breach_name": "Adobe",
        "breach_date": date(2019, 3, 12),
        "data_exposed": "Email, Password Hint",
        "severity": "Medium",
        "description": "Creative software customer database exposure.",
    },
    {
        "email": "stiti@gmail.com",
        "breach_name": "Adobe",
        "breach_date": date(2019, 3, 12),
        "data_exposed": "Email, Password Hint",
        "severity": "Medium",
        "description": "Creative software customer database exposure.",
    },
]


class Command(BaseCommand):
    help = "Import breach records from thedb.sql into MySQL"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing breach rows before importing",
        )

    def handle(self, *args, **options):
        sql_path = Path(__file__).resolve().parents[3] / "thedb.sql"
        if not sql_path.exists():
            self.stderr.write(self.style.ERROR(f"SQL file not found: {sql_path}"))
            return

        if options["clear"] and _table_exists("breaches"):
            deleted, _ = Breach.objects.all().delete()
            self.stdout.write(f"Cleared {deleted} existing breach row(s).")

        created = 0
        for row in BREACH_ROWS:
            _, was_created = Breach.objects.get_or_create(
                email=row["email"],
                breach_name=row["breach_name"],
                breach_date=row["breach_date"],
                defaults={
                    "data_exposed": row["data_exposed"],
                    "severity": row["severity"],
                    "description": row["description"],
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Import complete. {created} new row(s) added."))
        self.stdout.write("Test emails: john@gmail.com, john@yahoo.com, alice@gmail.com, stiti@gmail.com")
