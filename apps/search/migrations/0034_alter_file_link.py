# Generated by Django 4.0.6 on 2022-11-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0033_remove_generalizedhitssearch_authors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='link',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]