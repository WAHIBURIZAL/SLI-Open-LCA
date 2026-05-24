from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard_lca, name="dashboard_lca"),
    path("database/", views.database_lca, name="database_lca"),
    path("aktivitas/<int:aktivitas_id>/hapus/", views.hapus_aktivitas, name="hapus_aktivitas"),
]
