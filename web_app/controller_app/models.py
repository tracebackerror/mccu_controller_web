from django.db import models




class SLSCNetworkSettings(models.Model):
    ip_address = models.CharField(max_length=12)
    port_number = models.CharField(max_length=30)
