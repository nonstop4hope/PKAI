# Generated by Django 4.0.6 on 2022-10-26 13:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0013_alter_generalizedhitssearch_source_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalizedhitssearch',
            name='source_keywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, size=None),
        ),
    ]
