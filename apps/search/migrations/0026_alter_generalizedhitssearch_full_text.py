# Generated by Django 4.0.6 on 2022-10-29 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0025_alter_generalizedhitssearch_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalizedhitssearch',
            name='full_text',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
