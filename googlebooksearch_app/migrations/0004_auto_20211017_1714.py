# Generated by Django 3.2.8 on 2021-10-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlebooksearch_app', '0003_alter_book_publication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
