# Generated by Django 5.0.2 on 2024-02-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_fullname_user_full_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
