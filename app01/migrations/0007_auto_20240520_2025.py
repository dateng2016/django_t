# Generated by Django 3.2.9 on 2024-05-20 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_userinfo_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='data',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='size',
        ),
    ]
