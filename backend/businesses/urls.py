from django.urls import path
from .views import get_dashboard_data

urlpatterns = [
    path("api/dashboard/", get_dashboard_data, name="dashboard-data"),
]
