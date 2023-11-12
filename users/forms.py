from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'date_joined']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        # Disable the username field
        self.fields['username'].disabled = True

        # Display date_joined without hour and seconds
        self.fields['date_joined'] = forms.DateTimeField(
            widget=DateTimeInput(format='%Y-%m-%d'),
            input_formats=['%Y-%m-%d']
        )
        self.fields['date_joined'].disabled = True