# Generated by Django 4.0.6 on 2022-10-27 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0022_alter_generalizedhitssearch_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalizedhitssearch',
            name='full_text',
            field=models.TextField(default=None, null=True),
        ),
    ]
