# -*- coding: utf-8 -*-
"""
Migrate data from the legacy system

Before edX added support for custom registration pages,
we built our own from scratch for CME.
Now that the platform supports customization of the registration form,
we can do away with our custom implementation, after migrating the data.
"""
from __future__ import unicode_literals
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import migrations, models, transaction, IntegrityError

from ...models import ExtraInfo
from cme_registration.models import CmeUserProfile
from student.models import UserProfile


log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Migrate data from the legacy system
    """
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--insert',
            action='store_true',
            default=False,
            help='Insert new records into the database',
        )

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            try:
                info_old = CmeUserProfile.objects.get(pk=user.profile.id)
            except (UserProfile.DoesNotExist, CmeUserProfile.DoesNotExist):
                info_old = CmeUserProfile()
                log.info(
                    "CmeUserProfile not found for user_id: %(user_id)s",
                    {
                        'user_id': user.id,
                    }
                )
            info_new = ExtraInfo()
            info_new.id = user.id
            info_new.user_id = user.id
            info_new.address_1 = info_old.address_1 or ''
            info_new.address_2 = info_old.address_2 or ''
            info_new.affiliation = info_old.affiliation or 'Not affiliated with Stanford Medicine'
            info_new.birth_date = info_old.birth_date or '01/01'
            info_new.city = info_old.city_cme or ''
            info_new.country = info_old.country_cme or ''
            info_new.county_province = info_old.county_province or ''
            info_new.first_name = info_old.first_name or ''
            info_new.last_name = info_old.last_name or ''
            info_new.license_country = info_old.license_country or ''
            info_new.license_number = info_old.license_number or ''
            info_new.license_state = info_old.license_state or ''
            info_new.middle_initial = info_old.middle_initial or ''
            info_new.other_affiliation = info_old.other_affiliation or ''
            info_new.patient_population = info_old.patient_population or 'None'
            info_new.physician_status = info_old.physician_status or ''
            info_new.postal_code = info_old.postal_code or ''
            info_new.professional_designation = _clean_professional_designation(
                info_old.professional_designation
            )
            info_new.specialty = info_old.specialty or 'Other/None'
            info_new.stanford_department = info_old.stanford_department or ''
            info_new.state = info_old.state or ''
            info_new.sub_affiliation = info_old.sub_affiliation or ''
            info_new.sub_specialty = info_old.sub_specialty or ''
            info_new.sunet_id = info_old.sunet_id or ''
            if not kwargs['insert']:
                log.info(
                    "Insert of user_id=%(user_id)s faked",
                    {
                        'user_id': info_new.user_id,
                    }
                )
                continue
            try:
                with transaction.atomic():
                    info_new.save()
            except IntegrityError as error:
                log.warning(
                    "Insert of user_id=%(user_id)s failed; Integrity Error (%(error)s).",
                    {
                        'error': error,
                        'user_id': info_new.user_id,
                    }
                )
            else:
                log.info(
                    "Insert of user_id=%(user_id)s succeeded",
                    {
                        'user_id': info_new.user_id,
                    }
                )


def _clean_professional_designation(professional_designation):
    professional_designation = professional_designation or ''
    professional_designation = professional_designation.replace(' ', '')
    professional_designation = professional_designation or 'None'
    return professional_designation
