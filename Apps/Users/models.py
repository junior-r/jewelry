import os
import uuid

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_cleanup import cleanup
from django_countries.fields import CountryField


def user_directory_image_path(instance, filename):
    image_name = 'Users/{0}/Images/Profile/{1}'.format(instance.username.capitalize(), filename)
    full_path = os.path.join(settings.MEDIA_ROOT, image_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return image_name


@cleanup.select
class User(AbstractUser):
    ROLE_OPTIONS = (
        ('client', 'Cliente'),
        ('staff', 'Staff'),
        ('admin', 'Administrador'),
    )
    code = models.UUIDField(unique=True, blank=False, null=False, primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=user_directory_image_path, null=True, blank=True,
                              default="user_profile_placeholder.webp")
    country = CountryField(blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True, max_length=500)
    birth_date = models.DateField(null=True, blank=True)

    def get_avatar(self):
        if self.image and self.image.name != 'user_profile_placeholder.webp':
            return self.image.url
        elif SocialAccount.objects.filter(user__pk=self.code).exists():
            return SocialAccount.objects.get(user__pk=self.code).get_avatar_url()
        return os.path.join(settings.MEDIA_URL, 'user_profile_placeholder.webp')

    def get_full_name(self):
        if self.first_name and self.last_name:
            return '{0} {1}'.format(self.first_name, self.last_name)
        return self.username

    def get_role(self):
        if self.is_superuser:
            return self.ROLE_OPTIONS[2][1]
        elif self.is_staff:
            return self.ROLE_OPTIONS[1][1]
        return self.ROLE_OPTIONS[0][1]

    def get_role_display(self):
        badge = ('<span class="bg-{0}-100 text-{0}-800 text-sm font-medium px-2.5 py-0.5 rounded dark:bg-{0}-900 '
                 'dark:text-{0}-300">{1}</span>')
        role = self.get_role().capitalize()
        if self.is_superuser:
            return badge.format('yellow', role)
        elif self.is_staff:
            return badge.format('purple', role)
        return badge.format('blue', role)

    def get_absolute_url(self):
        return ""  # reverse('Users:profile', kwargs={'username': self.username})

    def get_update_url(self):
        return ""  # reverse('Users:update', kwargs={'pk': self.pk})

    def get_change_rol_url(self):
        return ""  # reverse('Users:change-role', kwargs={'pk': self.pk})

    def get_change_status_url(self):
        return ""  # reverse('Users:change-status', kwargs={'pk': self.pk})

    def __str__(self):
        return self.get_username()


@receiver(user_signed_up)
def user_complete_info(request, user, **kwargs):
    social_info = SocialAccount.objects.filter(user=user) if user else None
    if user and social_info and social_info.exists():
        user.first_name = social_info.get().extra_data.get('given_name', '')
        user.last_name = social_info.get().extra_data.get('family_name', '')
        user.save()


user_signed_up.connect(user_complete_info)