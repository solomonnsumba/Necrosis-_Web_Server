from django import forms


# Create Forms here
class ImageForm(forms.Form):
    images = forms.FileField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=224, required=True)
    password = forms.CharField(max_length=224, required=True)