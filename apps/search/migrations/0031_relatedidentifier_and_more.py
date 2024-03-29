# Generated by Django 4.0.6 on 2022-10-30 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0030_rename_issn_generalizedhitssearch_related_issn'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedIdentifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme', models.CharField(max_length=255)),
                ('identifier', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='generalizedhitssearch',
            name='related_issn',
        ),
        migrations.AddField(
            model_name='generalizedhitssearch',
            name='related_identifiers',
            field=models.ManyToManyField(blank=True, related_name='related_identifiers_list', to='search.relatedidentifier'),
        ),
    ]
