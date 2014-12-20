from django import forms
from django.forms.util import ErrorList

class DivErrorList(ErrorList):
	def __unicode__(self):
		return self.as_divs()

	def as_divs(self):
		if not self:
			return u''
		return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


class PatientRegistrationForm(forms.Form):
	username = forms.CharField()
	username.widget = forms.TextInput(attrs={'class':'form-control'})
	password = forms.CharField()
	password.widget = forms.PasswordInput(attrs={'class':'form-control'})
	firstname = forms.CharField()
	firstname.widget = forms.TextInput(attrs={'class':'form-control'})
	firstname.label = "First name"
	lastname = forms.CharField()
	lastname.widget = forms.TextInput(attrs={'class':'form-control'})
	lastname.label = "Last name"
	emailid = forms.EmailField()
	emailid.widget = forms.TextInput(attrs={'class':'form-control'})
	emailid.label = "Email id"
	mobNum = forms.CharField()
	mobNum.widget = forms.TextInput(attrs={'class':'form-control'})
	mobNum.label = "Mobile number"
	mobNum.help_text = "Your 10 digit mobile number"
	locality = forms.CharField()
	locality.widget = forms.TextInput(attrs={'class':'form-control'})
	locality.help_text="E.g. Banashankari, Koramangala"
