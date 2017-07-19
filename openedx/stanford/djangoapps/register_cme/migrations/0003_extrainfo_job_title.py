# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_cme', '0002_auto_20170515_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrainfo',
            name='job_title',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
