# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_cme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='physician_status',
            field=models.CharField(blank=True, max_length=8, choices=[('Active', 'Active'), ('Resident', 'Resident'), ('Fellow', 'Fellow'), ('Retired', 'Retired'), ('Inactive', 'Inactive')]),
        ),
    ]
