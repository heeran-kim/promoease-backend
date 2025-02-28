from django.urls import path
from ./views import get_dashboard_data

urlpatterns = [
    path("dashboard/", get_dashboard_data, name="dashboard-data"),
]
