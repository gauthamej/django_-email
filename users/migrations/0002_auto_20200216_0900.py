# Generated by Django 3.0.2 on 2020-02-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('designer', 'Designer'), ('production_house_staff', 'Production House Staff'), ('customer', 'Customer')], default='Designer', max_length=100, null=True),
        ),
    ]