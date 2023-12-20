# Generated by Django 4.2.4 on 2023-12-14 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_attendance_browser_attendance_ip_attendance_os_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hiringrecord',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birth Date'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='fb_url',
            field=models.TextField(blank=True, null=True, verbose_name='Facebook Profile URL'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='grammar_test',
            field=models.FileField(blank=True, null=True, upload_to='test_results/', verbose_name='Grammar Level Test'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='insta_url',
            field=models.TextField(blank=True, null=True, verbose_name='Instagram Profile URL'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='last_education',
            field=models.TextField(blank=True, null=True, verbose_name='Last Education'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='linkedin_url',
            field=models.TextField(blank=True, null=True, verbose_name='LinkedIn Profile URL'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='myers_briggs',
            field=models.FileField(blank=True, null=True, upload_to='test_results/', verbose_name='Myers Briggs Test'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='past_experience',
            field=models.TextField(blank=True, null=True, verbose_name='Past work experience'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='personality_test',
            field=models.FileField(blank=True, null=True, upload_to='test_results/', verbose_name='Similar Minds Personality Test'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='tiktok_url',
            field=models.TextField(blank=True, null=True, verbose_name='TikTok Profile URL'),
        ),
        migrations.AddField(
            model_name='hiringrecord',
            name='typing_test',
            field=models.FileField(blank=True, null=True, upload_to='test_results/', verbose_name='Typing Test'),
        ),
    ]