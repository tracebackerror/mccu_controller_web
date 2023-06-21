from django.db import models


class Satellite(models.Model):
    satellite_name = models.CharField(max_length=200, verbose_name="Satellite Name")
    longitude = models.CharField(max_length=200, verbose_name="Longitude")
    local_frequency = models.CharField(max_length=200, verbose_name="Local Frequency")
    rx_polarization = models.CharField(max_length=200, verbose_name="Rx Polarization")
    tx_polarization = models.CharField(max_length=200, verbose_name="Tx Polarization")
    time = models.CharField(max_length=200, verbose_name="Time")

class SafeMode(models.Model):
    password = models.CharField(max_length=200, verbose_name="SafeMode Password")

class SLSCNetworkSettings(models.Model):
    ip_address = models.CharField(max_length=12)
    port_number = models.CharField(max_length=30)
