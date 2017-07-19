# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django import forms

from .constants import *
from .models import ExtraInfo


class ExtraInfoForm(forms.ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model
    """
    def __init__(self, *args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].initial = '01/01'

    class Meta(object):
        error_messages = {
            'address_1': {
                'invalid': u'Your Address 1 must be at least 2 characters.',
                'required': u'Please enter your Address 1.',
            },
            'affiliation': {
                'required': u'Please select your Stanford Medicine Affiliation',
            },
            'birth_date': {
                'invalid': u'Date of birth not correct format (mm/dd).',
                'required': u'Please enter your Month and Day of Birth.',
            },
            'city': {
                'invalid': u'Your city must be at least 2 characters.',
                'required': u'Please enter your City.',
            },
            'country': {
                'invalid': "Invalid country: %(country)s.",
                'required': 'Please select your Country.',
            },
            'first_name': {
                'invalid': u'Your First Name must be at least 2 characters.',
                'required': u'Please enter your First Name.',
            },
            'last_name': {
                'invalid': u'Your Last Name must be at least 2 characters.',
                'required': u'Please enter your Last Name.',
            },
            'license_country': {
                'required': u'Please enter your License Country.',
            },
            'license_number': {
                'required': u'Please enter your License Number.',
            },
            'license_state': {
                'required': u'Please enter your License State.',
            },
            'middle_initial': {
                'invalid': u'Your middle initial must be at most 1 character.',
            },
            'other_affiliation': {
                'required': u'Please enter your Other Affiliation.',
            },
            'patient_population': {
                'required': u'Please enter your Patient Population.',
            },
            'physician_status': {
                'required': u'Please enter your Physician Status.',
            },
            'postal_code': {
                'required': u'Please enter your Postal Code.',
            },
            'professional_designation': {
                'required': u'Please select your Medical Designation or Professional Title.',
            },
            'specialty': {
                'required': u'Please select your Specialty.',
            },
            'stanford_department': {
                'required': u'Please select your Stanford Department.',
            },
            'state': {
                'required': u'Please select your State.',
            },
            'sunet_id': {
                'required': u'Please enter your SunetID.',
                'invalid': u'Your SunetID must be 3 to 8 characters in length.',
            },
        }
        fields = (
            'last_name',
            'first_name',
            'middle_initial',
            'birth_date',
            'gender',
            'dummy_header_professional_information',
            'professional_designation',
            'license_number',
            'license_country',
            'license_state',
            'physician_status',
            'patient_population',
            'specialty',
            'sub_specialty',
            'affiliation',
            'other_affiliation',
            'job_title',
            'stanford_department',
            'sunet_id',
            'dummy_header_professional_contact_information',
            'address_1',
            'address_2',
            'city',
            'country',
            'state',
            'county_province',
            'postal_code',
        )
        labels = {
            'affiliation': 'Stanford Medicine Affiliation',
            'birth_date': 'Month and Day of Birth',
            'county_province': 'International Province or Territory',
            'full_name': 'CANNOT BE CHANGED LATER',
            'job_title': 'Job Title or Position',
            'postal_code': 'Postal/Zip Code',
            'professional_designation': 'Medical Designation or Professional Title',
            'sunet_id': 'SUnet ID',
        }
        model = ExtraInfo

    def clean_address_1(self):
        address_1 = self.cleaned_data['address_1']
        if not(address_1):
            raise forms.ValidationError(
                self.fields['address_1'].error_messages['required'],
                code='required',
            )
        if len(address_1) < 2:
            raise forms.ValidationError(
                self.fields['address_1'].error_messages['invalid'],
                code='invalid',
            )
        return address_1

    def clean_affiliation(self):
        affiliation = self.cleaned_data['affiliation']
        if affiliation != 'Stanford University':
            return affiliation
        errors = []
        sunet_id = self.data['sunet_id']
        stanford_department = self.data['stanford_department']
        if not(sunet_id):
            errors.append({'sunet_id': 'required'})
        # SunetIDs can only be 3-8 characters
        elif not(3 <= len(sunet_id) <= 8):
            errors.append({'sunet_id': 'invalid'})
        if not(stanford_department):
            errors.append({'stanford_department': 'required'})
        for error in errors:
            for key in error:
                message = self.fields[key].error_messages[error[key]]
                self.add_error(key, message)
        return affiliation

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        parts = birth_date.split('/')
        if len(parts) is not 2:
            raise forms.ValidationError(
                self.fields['birth_date'].error_messages['invalid'],
                code='invalid',
            )
        # Set to 2012 as it was a leap year
        # which allows people to be born on Feb 29
        year = 2012
        month = parts[0]
        day = parts[1]
        try:
            datetime.date(year, int(month), int(day))
        except ValueError, e:
            raise forms.ValidationError(
                str(e),
                code='invalid',
            )
        return birth_date

    def clean_city(self):
        city = self.cleaned_data['city']
        if not city:
            raise forms.ValidationError(
                self.fields['city'].error_messages['required'],
                code='required',
            )
        if len(city) < 2:
            raise forms.ValidationError(
                self.fields['city'].error_messages['invalid'],
                code='invalid',
            )
        return city

    def clean_country(self):
        country = self.cleaned_data['country']
        if len(country) < 2:
            raise forms.ValidationError(
                self.fields['country'].error_messages['required'],
                code='invalid',
            )
        if country in DENIED_COUNTRIES:
            raise forms.ValidationError(
                self.fields['country'].error_messages['invalid'],
                code='invalid',
                params={
                    'country': country,
                },
            )
        return country

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 2:
            raise forms.ValidationError(
                self.fields['first_name'].error_messages['invalid'],
                code='invalid',
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 2:
            raise forms.ValidationError(
                self.fields['last_name'].error_messages['invalid'],
                code='invalid',
            )
        return last_name

    def clean_license_state(self):
        data = self.cleaned_data
        if data.get('license_country') == 'United States':
            if len(data.get('license_state', '')) < 2:
                raise forms.ValidationError(
                    self.fields['license_state'].error_messages['required'],
                    code='required',
                )
        return data.get('license_state')

    def clean_middle_initial(self):
        middle_initial = self.cleaned_data['middle_initial']
        if len(middle_initial) > 1:
            raise forms.ValidationError(
                self.fields['middle_initial'].error_messages['invalid'],
                code='invalid',
            )
        return middle_initial

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if len(postal_code) < 2:
            raise forms.ValidationError(
                self.fields['postal_code'].error_messages['required'],
                code='required',
            )
        return postal_code

    def clean_state(self):
        data = self.cleaned_data
        if data.get('country') == 'United States' and len(data.get('state', '')) < 2:
            raise forms.ValidationError(
                self.fields['state'].error_messages['required'],
                code='required',
            )
        return data.get('state')

    def clean(self):
        data = super(ExtraInfoForm, self).clean()
        self._validate_professional_designation(data)
        return data

    def _validate_professional_designation(self, data):
        if data.get('professional_designation') in PROFESSIONAL_DESIGNATIONS_WITH_EXTRA_REQUIREMENTS:
            for required in PROFESSIONAL_DESIGNATIONS_EXTRA_REQUIREMENTS:
                if len(data.get(required, '')) < 2:
                    value = self.fields[required].error_messages['required']
                    self.add_error(required, value)

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        label='Gender',
    )
    required_css_class = 'required'
    sub_specialty = forms.ChoiceField(
        choices=(
            ('', '---------'),
        ),
        label='Sub-Specialty',
        required=False,
    )
    dummy_header_professional_information = forms.CharField(
        required=False,
        label='Professional Information',
    )
    dummy_header_professional_contact_information = forms.CharField(
        required=False,
        label='Professional Contact Information',
    )
