# Generated by Django 3.2.3 on 2021-05-28 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20210528_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='user',
            new_name='creator',
        ),
    ]