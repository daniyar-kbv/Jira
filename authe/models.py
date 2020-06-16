from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.upload import avatar_path
from utils.validators import validate_file_size, validate_extension


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    bio = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.FileField(upload_to=avatar_path, validators=[validate_file_size, validate_extension], null=True,
                              blank=True)
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)