# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cme_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmeuserprofile',
            name='affiliation',
            field=models.CharField(blank=True, max_length=46, null=True, choices=[(b"Stanford Children's Health", b"Stanford Children's Health"), (b"Packard Children's Health Alliance", b"Packard Children's Health Alliance"), (b'Stanford Health Care', b'Stanford Health Care'), (b'Stanford University', b'Stanford University'), (b'University Healthcare Alliance', b'University Healthcare Alliance'), (b'Other', b'Other')]),
        ),
    ]
