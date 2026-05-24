import os
import tempfile
from pathlib import Path

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lca_project.settings")

application = get_wsgi_application()
app = application


def prepare_vercel_sqlite():
    if os.getenv("VERCEL") and os.getenv("DJANGO_VERCEL_AUTO_MIGRATE", "1") == "1":
        db_path = Path(tempfile.gettempdir()) / "db.sqlite3"
        if not db_path.exists():
            from django.core.management import call_command

            call_command("migrate", interactive=False, verbosity=0)


prepare_vercel_sqlite()
