from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


def _table_exists(name: str) -> bool:
    return name in connection.introspection.table_names()


class Command(BaseCommand):
    help = "Run migrations, import thedb.sql data, and seed dashboard tables"

    def handle(self, *args, **options):
        if not _table_exists("breaches"):
            from django.db.migrations.recorder import MigrationRecorder

            has_other_core_tables = any(
                _table_exists(t)
                for t in ("core_attackinfo", "core_emailcheck", "core_monthlybreachstat")
            )

            if has_other_core_tables:
                from core.models import Breach

                self.stdout.write("Creating missing breaches table...")
                with connection.schema_editor() as editor:
                    editor.create_model(Breach)
                MigrationRecorder.Migration.objects.update_or_create(
                    app="core",
                    name="0001_initial",
                    defaults={},
                )
            else:
                deleted, _ = MigrationRecorder.Migration.objects.filter(app="core").delete()
                if deleted:
                    self.stdout.write("Reset core migration history.")

        self.stdout.write("Step 1/3: Running migrations...")
        call_command("migrate", verbosity=1)

        self.stdout.write("Step 2/3: Importing breach data from thedb.sql...")
        call_command("import_db", clear=True, verbosity=1)

        self.stdout.write("Step 3/3: Seeding dashboard and attack intelligence data...")
        call_command("seed_data", verbosity=1)

        self.stdout.write(self.style.SUCCESS("Database setup complete."))
