from .models import ExtraInfo
from django.forms import ModelForm
from django import forms
import datetime



class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    # def __init__(self, *args, **kwargs):
    #     super(ExtraInfoForm, self).__init__(*args, **kwargs)
    #     # self.fields['favorite_movie'].error_messages = {
    #     #     "required": u"Please tell us your favorite movie.",
    #     #     "invalid": u"We're pretty sure you made that movie up.",
    #     # }

    # Construct dicts for sub-specialty, sub-affiliation dropdowns
    SUB_AFFILIATION_CHOICES = {
        'Packard_Childrens_Health_Alliance' : (('Bayside_Medical_Group', 'Bayside Medical Group'),
                                               ('Diablo_Valley_Child_Neurology',
                                                 'Diablo Valley Child Neurology'),
                                                ('Jagdip_Powar_Associates',
                                                 'Jagdip Powar, MD and Associates'),
                                                ('Judy_Fuentebella_Associates',
                                                 'Judy Fuentebella, MD  and Associates'),
                                                ('Livermore_Pleasanton_San_Ramon_Pediatrics_Group',
                                                 'Livermore Pleasanton San Ramon Pediatrics Group'),
                                                ('Pediatric_Cardiology_Medical_Group',
                                                 'Pediatric Cardiology Medical Group'),
                                                ('Pediatric_Cardiology_Associates',
                                                 'Pediatric Cardiology Associates'),
                                                ('Peninsula_Pediatrics', 'Peninsula Pediatrics'),
                                                ('Sabina_Ali_Associates',
                                                 'Sabina Ali, MD  and Associates')),
        'University_Healthcare_Alliance' : (('Affinity_Medical_Partners_Medical_Group', 'Affinity Medical Partners Medical Group (AMP)'),
                                            ('Bay_Valley_Medical_Group', 'Bay Valley Medical Group (BVMG)'),
                                            ('Cardiovascular_Consultants_Medical_Group', 'Cardiovascular Consultants Medical Group (CCMG)'),
                                            ('Menlo_Medical_Clinic', 'Menlo Medical Clinic (MMC)'))
    }

    SUB_SPECIALTY_CHOICES = {
        'Cardiovascular_Health': [
            ('Cardiac_Surgery', 'Cardiac Surgery'),
            ('Cardiology', 'Cardiology'),
            ('Cardiothoracic', 'Cardiothoracic'),
            ('Cardiothoracic_Surgery', 'Cardiothoracic Surgery'),
            ('Cardiovascular_Disease', 'Cardiovascular Disease'),
            ('Cath_Angio/Lab', 'Cath Angio/Lab'),
            ('Electrophysiology', 'Electrophysiology'),
            ('Interventional_Cardiology', 'Interventional Cardiology'),
        ],
        'Internal_Medicine': [
            ('Adolescent_Medicine', 'Adolescent Medicine'),
            ('Adult_Congenital_Heart_Disease', 'Adult Congenital Heart Disease'),
            ('Advanced_Heart_Failure_and_Transplant_Cardiology', 'Advanced Heart Failure and Transplant Cardiology'),
            ('Allergy_&_Immunology', 'Allergy & Immunology'),
            ('Cardiovascular_Disease', 'Cardiovascular Disease'),
            ('Clinical_Cardiac_Electrophysiology', 'Clinical Cardiac Electrophysiology'),
            ('Critical_Care_Medicine', 'Critical Care Medicine'),
            ('Endocrinology,_Diabetes,_&_Metabolism', 'Endocrinology, Diabetes, & Metabolism'),
            ('Gastroenterology', 'Gastroenterology'),
            ('Geriatric_Medicine', 'Geriatric Medicine'),
            ('Hematology', 'Hematology'),
            ('Hospice_&_Palliative_Medicine', 'Hospice & Palliative Medicine'),
            ('Hospital_Medicine,_Focused_Practice', 'Hospital Medicine, Focused Practice'),
            ('Infectious_Disease', 'Infectious Disease'),
            ('Interventional_Cardiology', 'Interventional Cardiology'),
            ('Medical_Oncology', 'Medical Oncology'),
            ('Nephrology', 'Nephrology'),
            ('Pulmonary_Disease', 'Pulmonary Disease'),
            ('Rheumatology', 'Rheumatology'),
            ('Sleep_Medicine', 'Sleep Medicine'),
            ('Sports_Medicine', 'Sports Medicine'),
        ],
        'Obstetrics_&_Gynecology': [
            ('Female_Pelvic_Medicine_and_Reconstructive_Surgery', 'Female Pelvic Medicine and Reconstructive Surgery'),
            ('Gynecologic_Oncology', 'Gynecologic Oncology'),
            ('Maternal-Fetal_Medicine', 'Maternal-Fetal Medicine'),
            ('Reproductive_Endocrinology_and_Infertility', 'Reproductive Endocrinology and Infertility'),
        ],
        'Oncology': [
            ('Hematology', 'Hematology'),
            ('Medical_Oncology', 'Medical Oncology'),
            ('Radiation_Oncology', 'Radiation Oncology'),
        ],
        'Orthopedics_&_Sports_Medicine': [
            ('Surgery', 'Surgery'),
        ],
        'Pediatrics': [
            ('Adolescent_Medicine', 'Adolescent Medicine'),
            ('Allergy,_Immunology,_&_Rheumatology', 'Allergy, Immunology, & Rheumatology'),
            ('Anesthesiology', 'Anesthesiology'),
            ('Cardiovascular_Health', 'Cardiovascular Health'),
            ('Complimentary_Medicine_&_Pain_Management', 'Complimentary Medicine & Pain Management'),
            ('Critical_Care_&_Pulmonology', 'Critical Care & Pulmonology'),
            ('Dental_Specialties', 'Dental Specialties'),
            ('Dermatology', 'Dermatology'),
            ('Emergency_Medicine_&_Trauma', 'Emergency Medicine & Trauma'),
            ('Endocrinology_&_Metabolism', ' Endocrinology & Metabolism'),
            ('Family_Medicine_&_Community_Health', 'Family Medicine & Community Health'),
            ('Gastroenterology_&_Hepatology', 'Gastroenterology & Hepatology'),
            ('Genetics_&_Genomics', 'Genetics & Genomics'),
            ('Gerontology', 'Gerontology'),
            ('Hematology', 'Hematology'),
            ('Infectious_Disease_&_Global_Health', 'Infectious Disease & Global Health'),
            ('Internal_Medicine', 'Internal Medicine'),
            ('Neonatology', 'Neonatology'),
            ('Nephrology', 'Nephrology'),
            ('Neurology_&_Neurologic_Surgery', 'Neurology & Neurologic Surgery'),
            ('Obstetrics_&_Gynecology', 'Obstetrics & Gynecology'),
            ('Oncology', 'Oncology'),
            ('Ophthalmology', 'Ophthalmology'),
            ('Orthopedics_&_Sports_Medicine', 'Orthopedics & Sports Medicine'),
            ('Otolaryngology_(ENT)', 'Otolaryngology (ENT)'),
            ('Pathology_&_Laboratory_Medicine', 'Pathology & Laboratory Medicine'),
            ('Preventative_Medicine_&_Nutrition', 'Preventative Medicine & Nutrition'),
            ('Psychiatry_&_Behavioral_Sciences', 'Psychiatry & Behavioral Sciences'),
            ('Radiology', 'Radiology'),
            ('Surgery', 'Surgery'),
            ('Urology', 'Urology'),
            ('Other/None', 'Other/None'),
        ],
        'Radiology': [
            ('Diagnostic_Radiology', 'Diagnostic Radiology'),
            ('Interventional_Radiology_and_Diagnostic_Radiology', 'Interventional Radiology and Diagnostic Radiology'),
            ('Medical_Physics', 'Medical Physics'),
            ('Radiation_Oncology', 'Radiation Oncology'),
            ('Therapeutic_Medical_Physics', 'Therapeutic Medical Physics'),
        ],
        'Surgery': [
            ('Complex_General_Surgical_Oncology', 'Complex General Surgical Oncology'),
            ('General_Surgery', 'General Surgery'),
            ('Hand_Surgery', 'Hand Surgery'),
            ('Hospice_and_Palliative_Medicine', 'Hospice and Palliative Medicine'),
            ('Pediatric_Surgery', 'Pediatric Surgery'),
            ('Surgical_Critical_Care', 'Surgical Critical Care'),
            ('Vascular_Surgery', 'Vascular Surgery'),
        ],
    }

    # first_name = forms.CharField(max_length=50, min_length=2, label='First name')
    # last_name = forms.CharField(max_length=50, min_length=2, label='Last name')
    birth_date = forms.CharField(max_length=5, initial='01/01', label='Month and Day of Birth')

    sub_specialty = forms.ChoiceField(choices=(("", "---------"),("a","a"),("b", "b")), label='Sub Specialty')

    class Meta(object):
        model = ExtraInfo
        fields = (
            'first_name', 'last_name', 'middle_initial', 'birth_date', 'professional_designation',
            'license_number', 'license_country', 'license_state', 'physician_status',
            'patient_population', 'specialty', 'sub_specialty', 'affiliation', #'other_affiliation', not used?
            'sub_affiliation', 'stanford_department', 'sunet_id', 'address_1', 'address_2', 'city',
            'state', 'county_province', 'postal_code', 'country'
        )

        # widgets = {
        #     'professional_designation': forms.Select(attrs = {'id':'yomama'}),
        #     'birth_date': forms.TextInput(attrs={'class': 'special', 'name':'special_name'})
        # }

    def _validate_birth_date(self, cleaned_data):
        date_parts = cleaned_data['birth_date'].split('/')
        if len(date_parts) is not 2:
            self.add_error('birth_data', 'Date of birth not in correct format (mm/dd)')
        else:
            dummy_year = 2012  # Set to 2012 as it was a leap year, which allows people to be born on Feb 29
            try:
                datetime.date(dummy_year, int(date_parts[0]), int(date_parts[1]))
            except ValueError, e:
                self.add_error('birth_data', str(e))

    def _validate_professional_fields(self, cleaned_data):
        required_fields_list = [{'license_number': 'Enter your license number'},
                                {'license_country': 'Choose your license country'},
                                {'physician_status': 'Enter your physician status'},
                                {'patient_population': 'Choose your patient population'},
                                {'specialty': 'Choose your specialty'},
                                ]

        if cleaned_data.get('professional_designation') in ['DO', 'MD', 'MD,PhD', 'MBBS']:
            for required_field in required_fields_list:
                for key, val in required_field.iteritems():
                    if len(cleaned_data.get(key)) < 2:
                        self.add_error(key, val)

        # license_state is required if license_country = United States
        if cleaned_data.get('license_country') == 'United States':
            if len(cleaned_data.get('license_state')) < 2:
                self.add_error('license_state', 'Choose your license state')

    def _validate_affiliation_fields(self, cleaned_data):
        """
        Checks affiliation fields
        """

        affiliation_fields_list = [
            {'Packard Children\'s Health Alliance': 'Enter your Packard Children\'s Health Alliance affiliation'},
            {'University Healthcare Alliance': 'Enter your University Healthcare Alliance affiliation'},
            ]

        for affiliation_field in affiliation_fields_list:
            for key, val in affiliation_field.iteritems():
                if cleaned_data.get('affiliation') == key and len(cleaned_data.get('sub_affiliation')) < 2:
                    self.add_error('sub_affiliation', val)

        required_fields_list = [{'sunet_id': 'Enter your SUNet ID'},
                                {'stanford_department': 'Choose your Stanford department'},
                                ]

        if cleaned_data.get('affiliation') == 'Stanford University':
            for required_field in required_fields_list:
                for key, val in required_field.iteritems():
                    if len(cleaned_data.get(key)) < 2:
                        self.add_error(key, val)

    def _validate_export_controls(self, cleaned_data):
        """
        Checks that we are US export control compliant.
        In keeping with the style of the rest of the app, returns failure dict if failed, else None
        """
        DENIED_COUNTRIES = ['Sudan',
                            'Korea, Democratic People\'s Republic Of',
                            'Iran, Islamic Republic Of',
                            'Cuba',
                            'Syrian Arab Republic',
                            ]

        country = cleaned_data['country']
        if country in DENIED_COUNTRIES:
            self.add_error('country', 'We are unable to register you at this time.')

    def clean(self):
        cleaned_data = super(ExtraInfoForm, self).clean()

        if len(cleaned_data['first_name']) < 2:
            self.add_error('first_name', 'First name must be at least 2 characters')
        if len(cleaned_data['last_name']) < 2:
            self.add_error('last_name', 'Last name must be at least 2 characters')
        if len(cleaned_data['middle_initial']) > 1:
            self.add_error('middle_initial', 'Middle initial must be at most 1 character')
        if len(cleaned_data['affiliation']) < 2:
            self.add_error('affiliaton', 'Choose your affiliation')
        if len(cleaned_data['address_1']) < 2:
            self.add_error('address_1', 'Enter your Address 1')
        if len(cleaned_data['city']) < 2:
            self.add_error('city', 'Enter your city')
        if len(cleaned_data['country']) < 2:
            self.add_error('country', 'Choose your country')
        if len(cleaned_data['postal_code']) < 2:
            self.add_error('postal_code', 'Enter your postal code')
        if cleaned_data['country'] == 'United States' and len(cleaned_data['state']) < 2:
            self.add_error('state', 'Choose your state')


        self._validate_birth_date(cleaned_data)
        self._validate_professional_fields(cleaned_data)
        self._validate_affiliation_fields(cleaned_data)
        self._validate_export_controls(cleaned_data)


        return cleaned_data



