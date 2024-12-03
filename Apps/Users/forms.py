from allauth.account.forms import SignupForm
from django import forms
from django.core.validators import FileExtensionValidator
from django_countries.fields import CountryField

from Apps.Users.models import User
from core.consts import error_messages, file_input_accept, allowed_image_extensions
from core.validators import small_file_size_validator


class DateInput(forms.DateInput):
    input_type = 'date'


class UserCreationForm(SignupForm):
    image = forms.ImageField(label='Foto de Perfil', required=False, error_messages=error_messages,
                             help_text='PNG, WEBP, AVIF, JPG o JPEG de hasta 1MB',
                             widget=forms.FileInput(attrs={'accept': file_input_accept}),
                             validators=[small_file_size_validator, FileExtensionValidator(allowed_image_extensions)])
    email = forms.EmailField(label='Correo electrónico*', required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'example@email.com',
    }))
    username = forms.CharField(label='Nombre de usuario', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'John123',
    }))
    first_name = forms.CharField(label='Nombres', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'John',
    }))
    last_name = forms.CharField(label='Apellidos', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Doe',
    }))
    password1 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={
        'placeholder': '**********',
    }))
    password2 = forms.CharField(label='Contraseña (de nuevo)', required=True, widget=forms.PasswordInput(attrs={
        'placeholder': '**********',
    }))

    def save(self, request):
        user = super(UserCreationForm, self).save(request)
        # Add your own processing here.
        user.image = self.cleaned_data['image']
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'image')


class UserUpdateForm(forms.ModelForm):
    image = forms.ImageField(label='Foto de Perfil', required=False, error_messages=error_messages,
                             help_text='PNG, WEBP, AVIF, JPG o JPEG de hasta 1MB',
                             widget=forms.FileInput(attrs={'accept': file_input_accept}),
                             validators=[small_file_size_validator, FileExtensionValidator(allowed_image_extensions)])
    email = forms.EmailField(label='Correo electrónico*', required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'example@email.com',
    }))
    username = forms.CharField(label='Nombre de usuario', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'John123',
    }))
    first_name = forms.CharField(label='Nombres', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'John',
    }))
    last_name = forms.CharField(label='Apellidos', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Doe',
    }))
    country = CountryField(blank=True).formfield()
    phone = forms.CharField(label='Número de teléfono', required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Número de teléfono',
    }), max_length=15)
    bio = forms.CharField(label='Biografía', required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Escribe algo sobre ti...',
        'rows': 3,
    }), max_length=500)
    birth_date = forms.DateField(label='Fecha de nacimiento', required=False, widget=DateInput(attrs={
        'placeholder': 'Fecha de nacimiento',
    }), input_formats=['%Y-%m-%d'], localize=True)

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.image = self.cleaned_data['image']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'image', 'country', 'phone', 'bio', 'birth_date')
