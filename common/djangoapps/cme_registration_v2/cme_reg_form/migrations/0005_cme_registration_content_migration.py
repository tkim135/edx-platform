# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, transaction, IntegrityError
from student.models import UserProfile

import logging


log = logging.getLogger(__name__)


def populate_cme_reg_form_extrainfo(apps, schema_editor):
    # Populate cme_reg_form_extrainfo with a copy of existing
    # records in cme_registration.
    CMERegistration = apps.get_model('cme_registration', 'CmeUserProfile')
    ExtraInfo = apps.get_model('cme_reg_form', 'ExtraInfo')

    cme_registrations = CMERegistration.objects.all()
    for cme_registration in cme_registrations:
        cme_reg_form = ExtraInfo()
        user_profile = UserProfile.objects.get(pk=cme_registration.userprofile_ptr_id)
        cme_reg_form.user_id = user_profile.user_id
        cme_reg_form.address_1 = cme_registration.address_1 or ''
        cme_reg_form.address_2 = cme_registration.address_2 or ''
        cme_reg_form.affiliation = cme_registration.affiliation or ''
        cme_reg_form.birth_date = cme_registration.birth_date or ''
        cme_reg_form.city = cme_registration.city_cme or ''
        cme_reg_form.country = cme_registration.country_cme or ''
        cme_reg_form.county_province = cme_registration.county_province or ''
        cme_reg_form.first_name = cme_registration.first_name or ''
        cme_reg_form.last_name = cme_registration.last_name or ''
        cme_reg_form.license_country = cme_registration.license_country or ''
        cme_reg_form.license_number = cme_registration.license_number or ''
        cme_reg_form.license_state = cme_registration.license_state or ''
        cme_reg_form.middle_initial = cme_registration.middle_initial or ''
        cme_reg_form.other_affiliation = cme_registration.other_affiliation or ''
        cme_reg_form.patient_population = cme_registration.patient_population or ''
        cme_reg_form.physician_status = cme_registration.physician_status or ''
        cme_reg_form.postal_code = cme_registration.postal_code or ''
        cme_reg_form.professional_designation = cme_registration.professional_designation or ''
        cme_reg_form.specialty = cme_registration.specialty or ''
        cme_reg_form.stanford_department = cme_registration.stanford_department or ''
        cme_reg_form.state = cme_registration.state or ''
        cme_reg_form.sub_affiliation = cme_registration.sub_affiliation or ''
        cme_reg_form.sub_specialty = cme_registration.sub_specialty or ''
        cme_reg_form.sunet_id = cme_registration.sunet_id or ''

        try:
            with transaction.atomic():
                cme_reg_form.save()
        except IntegrityError:
            log.warning("Insert of UserId: {user_id} failed with Integrity Error.".format(
                user_id=cme_reg_form.user_id
            ))


class Migration(migrations.Migration):

    dependencies = [
        ('cme_reg_form', '0004_auto_20170404_1408'),
        ('cme_registration', '0002_auto_20170313_1516'),
    ]

    operations = [
        migrations.RunPython(populate_cme_reg_form_extrainfo),
    ]
