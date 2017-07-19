# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ddt import ddt, data, unpack
from django.test import TestCase

from ..constants import DENIED_COUNTRIES
from ..constants import PROFESSIONAL_DESIGNATIONS_EXTRA_REQUIREMENTS
from ..constants import PROFESSIONAL_DESIGNATIONS_WITH_EXTRA_REQUIREMENTS
from ..forms import ExtraInfoForm


FORM_DATA_REQUIRED = {
    'address_1': '<address_1>',
    'affiliation': "Stanford Children's Health",
    'birth_date': '01/01',
    'city': '<city>',
    'country': 'Canada',
    'first_name': '<first_name>',
    'last_name': '<last_name>',
    'postal_code': '<postal_code>',
    'professional_designation': 'AuD',
}
FORM_FIELDS_OPTIONAL = [
    'address_2',
    'county_province',
    'license_country',
    'license_number',
    'license_state',
    'middle_initial',
    'other_affiliation',
    'patient_population',
    'physician_status',
    'specialty',
    'stanford_department',
    'state',
    'sub_specialty',
    'sunet_id',
]


@ddt
class ExtraInfoFormTest(TestCase):

    def setUp(self):
        self.data = dict(FORM_DATA_REQUIRED)

    def test_valid(self):
        data = self.data
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertTrue(is_valid)

    @data(*zip(FORM_DATA_REQUIRED.keys(), [None, '']))
    @unpack
    def test_missing_always_required_fields_empty(self, field, value):
        """
        Assert that form is invalid if any required field is empty or nothing
        """
        data = self.data
        data[field] = None
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    @data(*FORM_DATA_REQUIRED.keys())
    def test_missing_always_required_fields_missing(self, field):
        """
        Assert that form is invalid if any required field is missing
        """
        data = self.data
        del data[field]
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    @data(*zip(FORM_FIELDS_OPTIONAL, [None, '']))
    @unpack
    def test_empty_optional_fields_empty(self, field, value):
        """
        Assert that form is valid with optional fields empty or nothing
        """
        data = self.data
        data[field] = value
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertTrue(is_valid)

    @data('/1', '1/', '1', '20/20', '001/001', 'hello')
    def test_birthdate_format(self, birth_date):
        data = self.data
        data['birth_date'] = birth_date
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    @data(*[
        'professional_designation',
        'license_country',
        'license_state',
        'physician_status',
        'patient_population',
        'specialty',
        'affiliation',
        'stanford_department',
        'country',
        'state',
    ])
    def test_invalid_choices(self, field):
        data = self.data
        data[field] = 'INVALID'
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    @data(*zip(
        PROFESSIONAL_DESIGNATIONS_WITH_EXTRA_REQUIREMENTS,
        PROFESSIONAL_DESIGNATIONS_EXTRA_REQUIREMENTS,
    ))
    @unpack
    def test_professional_designation_dependencies(self, designation, _dummy):
        data = self.data
        data['professional_designation'] = designation
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    @data(
        ('license_', None, False),
        ('license_', 'ZA', False),
        ('license_', 'CA', True),
        ('', None, False),
        ('', 'ZA', False),
        ('', 'CA', True),
    )
    @unpack
    def test_usa_dependencies(self, prefix, state, expected):
        data = self.data
        country_field = prefix + 'country'
        state_field = prefix + 'state'
        data[country_field] = 'United States'
        data[state_field] = state
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertTrue(is_valid is expected, form.errors)

    @data(*DENIED_COUNTRIES)
    def test_export_countries(self, country):
        data = self.data
        data['country'] = country
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    @data(None, '', 'ab', 'longsunet')
    def test_affiliation_sunet_id(self, sunet_id):
        data = self.data
        data['affiliation'] = 'Stanford University'
        data['stanford_department'] = 'Medicine'
        data['sunet_id'] = sunet_id
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    @data(None, '', 'invalid_department')
    def test_affiliation_stanford_department(self, stanford_department):
        data = self.data
        data['affiliation'] = 'Stanford University'
        data['stanford_department'] = stanford_department
        data['sunet_id'] = 'sunet_id'
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)

    def test_postal_code_too_short(self):
        data = self.data
        data['postal_code'] = '1'
        form = ExtraInfoForm(data)
        is_valid = form.is_valid()
        self.assertFalse(is_valid)
