from django import forms

from .models import Account


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "password", 'name': "password", 'placeholder': '. . . . . . . .'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "confirm_password", 'name': "confirm_password", 'placeholder': '. . . . . . . .'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'gender', 'phone_number', 'username']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
    def __int__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widgets.attrs['placeholder'] = 'Enter First Name'
        self.fields['first_name'].widgets.attrs['id'] = 'first_name'
        self.fields['first_name'].widgets.attrs['name'] = 'first_name'

        self.fields['last_name'].widgets.attrs['placeholder'] = 'Enter Last Name'
        self.fields['last_name'].widgets.attrs['id'] = 'last_name'
        self.fields['last_name'].widgets.attrs['name'] = 'last_name'

        self.fields['phone_number'].widgets.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['phone_number'].widgets.attrs['id'] = 'phone_number'
        self.fields['phone_number'].widgets.attrs['name'] = 'phone_number'

        self.fields['username'].widgets.attrs['placeholder'] = 'Enter Username'
        self.fields['username'].widgets.attrs['id'] = 'username'
        self.fields['username'].widgets.attrs['name'] = 'username'

        self.fields['gender'].widgets.attrs['placeholder'] = 'Select Gender'
        self.fields['gender'].widgets.attrs['id'] = 'gender'
        self.fields['gender'].widgets.attrs['name'] = 'gender'

        self.fields['email'].widgets.attrs['placeholder'] = 'Enter Your Email'
        self.fields['email'].widgets.attrs['id'] = 'email'
        self.fields['email'].widgets.attrs['name'] = 'email'

