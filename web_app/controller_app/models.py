from django.db import models


class Satellite(models.Model):
    satellite_name = models.CharField(max_length=200, verbose_name="Satellite Name")
    line1 = models.TextField(verbose_name="Line1")
    line2 = models.TextField(verbose_name="Line2")
    local_frequency = models.CharField(max_length=200, verbose_name="Local Frequency")


class SafeMode(models.Model):
    password = models.CharField(max_length=200, verbose_name="SafeMode Password")

class SLSCNetworkSettings(models.Model):
    ip_address = models.CharField(max_length=12)
    port_number = models.CharField(max_length=30)
