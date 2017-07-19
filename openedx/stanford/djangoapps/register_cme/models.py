# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from .constants import *

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
SUB_SPECIALTY_CHOICES = {
    specialty.get('key', specialty['display']): specialty['sub_specialties']
    for specialty in SPECIALTIES
    if 'sub_specialties' in specialty
}


class ExtraInfo(models.Model):
    """
    This model contains extra fields that will be saved when a user registers.
    """
    user = models.OneToOneField(
        USER_MODEL,
    )
    last_name = models.CharField(
        max_length=50,
    )
    first_name = models.CharField(
        max_length=50,
    )
    middle_initial = models.CharField(
        blank=True,
        max_length=1,
    )
    birth_date = models.CharField(
        max_length=5,
    )
    job_title = models.CharField(
        blank=True,
        max_length=50,
    )
    professional_designation = models.CharField(
        choices=PROFESSIONAL_DESIGNATION_CHOICES,
        max_length=7,
    )
    license_number = models.CharField(
        blank=True,
        max_length=20,
    )
    license_country = models.CharField(
        blank=True,
        choices=COUNTRY_CHOICES,
        max_length=42,
    )
    license_state = models.CharField(
        blank=True,
        choices=STATE_CHOICES,
        max_length=2,
    )
    physician_status = models.CharField(
        blank=True,
        choices=PHYSICIAN_STATUS_CHOICES,
        max_length=8,
    )
    patient_population = models.CharField(
        blank=True,
        choices=PATIENT_POPULATION_CHOICES,
        max_length=9,
    )
    specialty = models.CharField(
        blank=True,
        choices=[
            (specialty.get('key', specialty['display']), specialty['display'])
            for specialty in SPECIALTIES
        ],
        max_length=40,
    )
    sub_specialty = models.CharField(
        blank=True,
        max_length=50,
    )
    affiliation = models.CharField(
        choices=[
            (affiliation, affiliation)
            for affiliation in AFFILIATIONS
        ],
        max_length=43,
    )
    other_affiliation = models.CharField(
        blank=True,
        max_length=50,
    )
    sub_affiliation = models.CharField(
        blank=True,
        max_length=46,
    )
    stanford_department = models.CharField(
        blank=True,
        choices=DEPARTMENT_CHOICES,
        max_length=42,
    )
    sunet_id = models.CharField(
        blank=True,
        max_length=33,
    )
    address_1 = models.CharField(
        max_length=250
    )
    address_2 = models.CharField(
        blank=True,
        max_length=150,
    )
    city = models.CharField(
        max_length=75,
    )
    country = models.CharField(
        choices=COUNTRY_CHOICES,
        max_length=42,
    )
    state = models.CharField(
        blank=True,
        choices=STATE_CHOICES,
        max_length=2,
    )
    county_province = models.CharField(
        blank=True,
        max_length=50,
    )
    postal_code = models.CharField(
        max_length=20,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
    )
    modified_date = models.DateTimeField(
        auto_now=True,
    )

    @classmethod
    def lookup_professional_designation(cls, user):
        designation = None
        designations = cls.objects.filter(user=user).values('professional_designation')
        if len(designations):
            designation = designations[0]['professional_designation']
        return designation
