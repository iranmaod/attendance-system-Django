# Generated by Django 4.2.4 on 2023-12-15 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_alter_note_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='browser',
            new_name='browser_end',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='ip',
            new_name='browser_start',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='os',
            new_name='ip_end',
        ),
        migrations.AddField(
            model_name='attendance',
            name='ip_start',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='os_end',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='os_start',
            field=models.TextField(blank=True, null=True),
        ),
    ]
