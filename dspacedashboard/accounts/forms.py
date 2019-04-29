from django import forms

from dspacedashboard.accounts.models import User

class CreateUserForm(forms.ModelForm):

	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(
		label='Confirmação de Senha', widget=forms.PasswordInput
	)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Confirmação de senha incorreta")
		return password2

	def save(self, commit=True):
		user = super(CreateUserForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user

	class Meta:
		model = User
		fields = ['name', 'username', 'email', 'is_staff']


class UpdateUserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username','email','name', 'is_staff', 'is_active']