# Generated by Django 4.0.6 on 2022-12-14 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0035_generalizedhitssearch_favourite'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalizedhitssearch',
            name='user',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
