# Generated by Django 4.0.6 on 2022-10-23 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_generalizedhitssearch_access_right_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalizedhitssearch',
            name='citations_number',
            field=models.IntegerField(default=0),
        ),
    ]