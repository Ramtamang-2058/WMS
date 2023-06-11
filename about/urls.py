from django.urls import path
from . import views

urlpatterns = [
    #user view for all
    path('toilet', views.toilets, name="toilet"),
    path('contact', views.contact, name="contact"),

    path('bin', views.dustbins, name="bin"),
    path('about', views.user_about, name="about"),

    path('service', views.service, name="service"),

    path('', views.home, name="home"),

    #authentication
    path('login', views.user_login, name="login"),
    path('account/change_password', views.change_password, name="change_password"),
    path('account/password/success', views.change_success, name="change_success"),


    #administrator 
    path('dashboard/admin', views.admin_dashboard,  name="admin_dashboard"),
    path('dashboard/feedback', views.admin_feedback,  name="feedback"),
    path('dashboard/vendor', views.vendor_dashboard, name="vendor_dashboard"),
    path('vendors/list', views.vendor, name="vendors"),
    path('dashboard/bins/<str:category_name>', views.bins_view, name="bins"),
    path('bin/view/<str:latitude>', views.view_dustbin, name="chart"),
    #register vendor
    path('dashboard/vendor/add', views.add_vendor, name='add_vendor'),
    path('dashboard/vendor/edit/<int:id>', views.edit_vendor, name='edit_vendor'),


    #delete
    path('delete/<int:id>', views.delete, name="delete"),

    #logout
    path('logout', views.logout_view, name='logout'),

    #user 
    path('about', views.about_us, name="about"),

    #vendor
    path('map/route', views.view_map, name='map'),
    path('bins/all', views.vendor_bins, name="vendors_bins"),
    path('my/details', views.vendor_profile, name = 'profile'),
    path('my/details/<int:id>', views.vendor_detail, name = 'vendor_profile'),


    #notification read
    path('mark-notification-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),


]