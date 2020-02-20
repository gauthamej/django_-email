import datetime
import random
import string
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


TOKEN_CHARS = string.ascii_letters + string.digits

def generate_token():
    token = None
    while token is None:
        token = ''.join([random.choice(TOKEN_CHARS) for _ in range(25)])
        try:
            Token.objects.get(key=token)
            token = None
        except Token.DoesNotExist:
            pass
    return token

class User(AbstractUser):
    phone_number = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    username=None
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    coordinates = ArrayField(base_field=models.FloatField(), null=True, blank=True)
    
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    USER_TYPE=(
        ('designer', 'Designer'),
        ('production_house_staff','Production House Staff'),
        ('customer','Customer')
    )
    user_type = models.CharField(max_length = 100, choices = USER_TYPE, default = 'Designer', null=True, blank=True )

    def __str__(self):
        return f'{self.name}'


class Designer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_radius = models.FloatField(default=5, null=True, blank=True)

    def __str__(self):
        return f'{self.user.name}'


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user.name}'


class Token(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @classmethod
    def create_token(self, user):
        key = generate_token()
        expires_at = datetime.datetime.now() + datetime.timedelta(days=settings.AUTH_TOKEN_EXPIRY_DAYS)
        token = Token.objects.create(user=user, key=key, expires_at=expires_at)
        return token
