# Author: Dwiref
# Updated: 12/20/2019

from django import forms

class CriteriaForm(forms.Form):

    criteria_1 = forms.CharField(max_length = 255)
    criteria_2 = forms.CharField(max_length = 255)
    criteria_3 = forms.CharField(max_length = 255)
