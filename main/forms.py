from cProfile import label
from pyexpat import model
from attr import fields
from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ProdutoFeedback, UserEnderecoLista
from allauth.account.forms import LoginForm, UserForm, SignupForm


class SignupForm(SignupForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control'},),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
			'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
			'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
			'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
			'password2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
      }

# Formulario entrar 

class EntrarFormulario(LoginForm):
    class Meta:
        model = LoginForm
        fields = ('username', 'password1')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
			'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
   }

class ReviewAdd(forms.ModelForm):
	class Meta:
		model = ProdutoFeedback
		fields = ('review_text', 'review_rating')

# AddressBook Add Form


class FormListaEndereco(forms.ModelForm):
	class Meta:
		model = UserEnderecoLista
		labels = {
					'cep': 'Insira o Cep',
     				'status': 'definir ativo',

				}
		fields = ('cep', 'endereco', 'bairro', 'cidade',
		          'estado', 'telefone', 'whathsapp', 'status')
		widgets = {
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o Cep', 'id': 'cep', 'onblur': 'pesquisacep(this.value);'},),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
            'whathsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
           }

# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')
		widgets = {
					'first_name': forms.TextInput(attrs={'class': 'form-control'},),
					'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
					'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),
					'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''},),					
				}