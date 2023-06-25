# Generated by Django 4.2.2 on 2023-06-25 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller_app', '0003_safemode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='satellite',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='satellite',
            name='rx_polarization',
        ),
        migrations.RemoveField(
            model_name='satellite',
            name='time',
        ),
        migrations.RemoveField(
            model_name='satellite',
            name='tx_polarization',
        ),
        migrations.AddField(
            model_name='satellite',
            name='line1',
            field=models.TextField(default=1, verbose_name='Line1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='satellite',
            name='line2',
            field=models.TextField(default=1, verbose_name='Line2'),
            preserve_default=False,
        ),
    ]
