from django import forms
class SimpleForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    
f = SimpleForm()
print(f.as_p())