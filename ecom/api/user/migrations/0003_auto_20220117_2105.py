# Generated by Django 3.0.8 on 2022-01-17 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210125_0009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['email']},
        ),
    ]
