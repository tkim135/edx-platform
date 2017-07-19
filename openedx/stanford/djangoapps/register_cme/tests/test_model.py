# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings

from ..models import ExtraInfo
from .test_form import FORM_DATA_REQUIRED


TEST_FEATURES = settings.FEATURES.copy()
TEST_FEATURES['USE_CME_REGISTRATION'] = True


@override_settings(FEATURES=TEST_FEATURES)
class ExtraInfoTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='1234',
        )
        self.user.save()

    def test_create_good(self):
        self.info = ExtraInfo(**FORM_DATA_REQUIRED)
        self.info.user = self.user
        saved = self.info.save()

    def test_db_lookup_good(self):
        self.info = ExtraInfo(
            user=self.user,
            **FORM_DATA_REQUIRED
        )
        saved = self.info.save()
        info = ExtraInfo.objects.get(user=self.user)

    def test_db_lookup_bad(self):
        user = User.objects.create_user(
            username='test2',
            password='1234',
        )
        self.info = ExtraInfo(
            user=self.user,
            **FORM_DATA_REQUIRED
        )
        self.info.save()
        with self.assertRaises(ExtraInfo.DoesNotExist):
            info = ExtraInfo.objects.get(user=user)

    def test_lookup_professional_designation(self):
        self.info = ExtraInfo(
            user=self.user,
            **FORM_DATA_REQUIRED
        )
        saved = self.info.save()
        result = ExtraInfo.lookup_professional_designation(self.user)
        self.assertEquals(result, FORM_DATA_REQUIRED['professional_designation'])
