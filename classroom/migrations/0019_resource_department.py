# Generated by Django 5.0.2 on 2024-03-02 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_department_alter_user_department'),
        ('classroom', '0018_alter_resource_file_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.department'),
        ),
    ]
