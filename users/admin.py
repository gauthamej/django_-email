from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from users import models



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.User
        fields = '__all__'


class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    model = models.User
    ordering = ['name', 'email']

CustomUserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'phone_number',
                                             'address')

admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Designer)
admin.site.register(models.Customer)
