# Generated by Django 4.2.7 on 2023-11-30 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0003_book_scrapedurl_is_scrapped'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
