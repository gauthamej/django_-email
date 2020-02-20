from django import forms
from users.models import User
from users.models import Designer
import random
import string
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from antway_server import settings

class UserForm(forms.ModelForm):

    class Meta:
        model= User
        fields = ('name','email','phone_number','address','user_type')

    def save(self, commit=True):
        
        N=8
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        user = super(UserForm, self).save(commit=False)
        print(password)
        user.set_password(password)
        self.password = password
        if commit:
            user.save()
            
        usertype=self.cleaned_data['user_type']
        if usertype=="customer":
            Designer.objects.create(user=user)
        return user
        