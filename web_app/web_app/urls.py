from django.contrib import admin
from django.urls import path
from controller_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginPage.as_view(), name="login"),
    path('dashboard', views.DashboardPage.as_view(), name="login"),
    path('profile', views.ProfilePage.as_view(), name="profile"),

    path('safemode', views.safemode_command, name="safemode"),
    path('home', views.home_command, name="home"),
    path('shutdown', views.shutdown_command, name="shutdown"),
    path('restart', views.restart_command, name="restart"),

    path('logout', views.logout_view, name="logout"),
    path('settings', views.SettingsPage.as_view(), name="settings"),
    path('change_password/', views.change_password, name='change_password'),
    path('csv_stream', views.stream_csv, name='csv_stream'),

    path('satellites/', views.satellite_list, name='satellite_list'),
    path('satellites/<int:satellite_id>/get/', views.get_satellite, name='get_satellite'),
    path('satellites/<int:satellite_id>/set/', views.set_satellite, name='set_satellite'),
    path('satellites/<int:satellite_id>/load/', views.load_satellite, name='load_satellite'),

]
