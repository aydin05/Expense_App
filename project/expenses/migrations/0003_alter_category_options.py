# Generated by Django 4.1.4 on 2023-01-09 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',)},
        ),
    ]
