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
            field=models.CharField(blank=True, max_length=46, null=True, choices=[(b"Stanford Children's Health", b"Stanford Children's Health"), (b"Packard Children's Health Alliance (PCHA)", b"Packard Children's Health Alliance (PCHA)"), (b'Stanford Health Care', b'Stanford Health Care'), (b'Stanford University', b'Stanford University'), (b'University Healthcare Alliance (UHA)', b'University Healthcare Alliance (UHA)'), (b'Not affiliated with Stanford Medicine', b'Not affiliated with Stanford Medicine')]),
        ),
        migrations.AlterField(
            model_name='cmeuserprofile',
            name='specialty',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(b'Allergy,_Immunology,_&_Rheumatology', b'Allergy, Immunology, & Rheumatology'), (b'Anesthesiology', b'Anesthesiology'), (b'Cardiovascular_Health', b'Cardiovascular Health'), (b'Complimentary_Medicine_&_Pain_Management', b'Complimentary Medicine & Pain Management'), (b'Critical_Care_&_Pulmonology', b'Critical Care & Pulmonology'), (b'Dental_Specialties', b'Dental Specialties'), (b'Dermatology', b'Dermatology'), (b'Emergency_Medicine_&_Trauma', b'Emergency Medicine & Trauma'), (b'Endocrinology_&_Metabolism', b'Endocrinology & Metabolism'), (b'Family_Medicine_&_Community_Health', b'Family Medicine & Community Health'), (b'Gastroenterology_&_Hepatology', b'Gastroenterology & Hepatology'), (b'Genetics_&_Genomics', b'Genetics & Genomics'), (b'Gerontology', b'Gerontology'), (b'Hematology', b'Hematology'), (b'Infectious_Disease_&_Global_Health', b'Infectious Disease & Global Health'), (b'Internal_Medicine', b'Internal Medicine'), (b'Nephrology', b'Nephrology'), (b'Neurology_&_Neurologic_Surgery', b'Neurology & Neurologic Surgery'), (b'Obstetrics_&_Gynecology', b'Obstetrics & Gynecology'), (b'Oncology', b'Oncology'), (b'Ophthalmology', b'Ophthalmology'), (b'Orthopedics_&_Sports_Medicine', b'Orthopedics & Sports Medicine'), (b'Otolaryngology_(ENT)', b'Otolaryngology (ENT)'), (b'Pathology_&_Laboratory_Medicine', b'Pathology & Laboratory Medicine'), (b'Pediatrics', b'Pediatrics'), (b'Preventative_Medicine_&_Nutrition', b'Preventative Medicine & Nutrition'), (b'Psychiatry_&_Behavioral_Sciences', b'Psychiatry & Behavioral Sciences'), (b'Radiology', b'Radiology'), (b'Surgery', b'Surgery'), (b'Urology', b'Urology'), (b'Other/None', b'Other/None')]),
        ),
    ]
