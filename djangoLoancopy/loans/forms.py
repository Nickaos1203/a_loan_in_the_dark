from django import forms
from .models import STATE_CHOICES, BANK_CHOICES, NAICS_CHOICES

class LoanForm(forms.Form):
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
    bank = forms.ChoiceField(choices=BANK_CHOICES, required=False)
    naics = forms.ChoiceField(choices=NAICS_CHOICES, required=False)
    
    rev_line_cr = forms.ChoiceField(choices=[(None, 'N/A'), (0, 'Non'), (1, 'Oui')], required=False)
    low_doc = forms.ChoiceField(choices=[(None, 'N/A'), (0, 'Non'), (1, 'Oui')], required=False)
    new_exist = forms.ChoiceField(choices=[(None, 'N/A'), (0, 'Non'), (1, 'Oui')], required=False)
    has_franchise = forms.ChoiceField(choices=[(None, 'N/A'), (0, 'Non'), (1, 'Oui')], required=False)
    recession = forms.ChoiceField(choices=[(None, 'N/A'), (0, 'Non'), (1, 'Oui')], required=False)
    urban_rural = forms.ChoiceField(choices=[(None, 'N/A'), (0, 'Non'), (1, 'Oui')], required=False)

    create_job = forms.IntegerField(required=False, min_value=0)
    retained_job = forms.IntegerField(required=False, min_value=0)
    no_emp = forms.IntegerField(required=False, min_value=0)

    term = forms.IntegerField(required=True, min_value=1)
    gr_appv = forms.FloatField(required=True, min_value=0.0)
