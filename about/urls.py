from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name="login"),
    path('dashboard/admin', views.admin_dashboard,  name="admin_dashboard"),
    path('dashboard/vendor', views.vendor_dashboard, name="vendor_dashboard"),
]