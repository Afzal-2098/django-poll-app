from django import forms
from .models import Question, Choice, Vote, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm
from django.core.validators import RegexValidator


# Form for creating new polls.
class CreatePollForm(forms.ModelForm):
    option1 = forms.CharField(required=True, label='Option 1', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    option2 = forms.CharField(required=True, label='Option 2', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    option3 = forms.CharField(required=True, label='Option 3', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    option4 = forms.CharField(required=True, label='Option 4', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ["text", "option1", "option2", "option3", "option4"]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 20, 'placeholder':'Write Your Question'}),
        }


# Form for registering new users.
class UserRegistraionForm(UserCreationForm):
    first_name = forms.CharField(required=True,label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirmed Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone']
        labals = {'email': 'Email'}
        widget = {'username': forms.TextInput(attrs={'class':'form-control'})}


# Form for Logged the user in.
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


# Form for resetting the account password. 
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=250, widget=forms.EmailInput(attrs={'autofocus':'email', 'class':'form-control'}))
