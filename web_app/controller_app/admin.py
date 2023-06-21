from django.contrib import admin
from .models import SLSCNetworkSettings, Satellite, SafeMode

admin.site.register(SLSCNetworkSettings)
admin.site.register(Satellite)
admin.site.register(SafeMode)
