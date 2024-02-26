# Generated by Django 5.0.2 on 2024-02-26 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0005_alter_room_room_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_password',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='room_privacy',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], max_length=255, null=True),
        ),
    ]
