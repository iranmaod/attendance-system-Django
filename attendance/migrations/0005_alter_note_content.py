# Generated by Django 4.2.4 on 2023-12-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_alter_hiringrecord_fb_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
