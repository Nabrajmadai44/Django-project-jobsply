import re
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["email", "first_name", "middle_name", "last_name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):  # def validate() for serializers
        cleaned_data = super().clean()
        print(cleaned_data)
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords didn't match")
        return cleaned_data

    # def clean_password1(self):  # validate_password1 for serializers
    #     password1 = self.cleaned_data.get("password1")
    #     print(password1)
    #     if len(password1) < 8:
    #         print("Length Validation")
    #         raise forms.ValidationError("Password must be 8 characters long!")
    #     if not re.search(r'\d', password1) or not re.search(r'[A-Za-z]', password1):
    #         print("Numbers and chars")
    #         raise forms.ValidationError("Password must contain both numbers and characters.")
    #     return password1


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})