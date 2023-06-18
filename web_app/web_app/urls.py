from django.contrib import admin
from django.urls import path
from controller_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginPage.as_view(), name="login"),
    path('dashboard', views.DashboardPage.as_view(), name="login"),
    path('profile', views.ProfilePage.as_view(), name="profile"),
    path('logout', views.logout_view, name="logout"),
    path('settings', views.SettingsPage.as_view(), name="settings"),
    path('change_password/', views.change_password, name='change_password'),
]
