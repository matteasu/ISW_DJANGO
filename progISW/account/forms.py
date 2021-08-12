from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from account.models import Account


class RegistrationForm(UserCreationForm):
	class Meta:
		model = Account
		fields = ("playerID", "password1", "password2")


class LoginForm(forms.ModelForm):
	# specifico come voglio il campo password in modo che quest'ultima venga nascosta
	password = forms.CharField(label = "Password", widget = forms.PasswordInput)

	class Meta:
		model = Account
		fields = ("playerID", "password")

	# logica eseguita prima dell'inivio dei dati
	def clean(self):
		if self.is_valid():
			playerID = self.cleaned_data['playerID']
			password = self.cleaned_data['password']
			# verifico se le credenziali sono valide, altrimenti mostro dei messaggi di errore
			if not authenticate(playerID = playerID, password = password):
				raise ValidationError("Credenziali non valide")
		else:
			raise ValidationError("Form non valido")