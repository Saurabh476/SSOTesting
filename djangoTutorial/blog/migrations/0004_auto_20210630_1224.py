# Generated by Django 3.2.4 on 2021-06-30 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentprofiles',
            options={'verbose_name': 'StudentProfiles'},
        ),
        migrations.AlterModelTable(
            name='studentprofiles',
            table='StudentProfiles',
        ),
    ]
