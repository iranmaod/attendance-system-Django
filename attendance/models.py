from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Attendance(models.Model):
  user_id = models.IntegerField()
  date = models.DateField(null=True, blank = True)
  start_time = models.DateTimeField(null=True, blank = True)
  end_time = models.DateTimeField(null=True, blank = True)
  task = models.TextField(null=True, blank = True)
  ended = models.TextField(default=0)
  ip_start = models.TextField(null=True, blank = True)
  os_start = models.TextField(null=True, blank = True)
  browser_start = models.TextField(null=True, blank = True)
  ip_end = models.TextField(null=True, blank = True)
  os_end = models.TextField(null=True, blank = True)
  browser_end = models.TextField(null=True, blank = True)

class Breaks(models.Model):
  break_time = models.DateTimeField(null=True, blank = True)
  back_time = models.DateTimeField(null=True, blank = True)
  reason = models.TextField(null=True, blank = True)
  attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=True)

class Tasks(models.Model):
  start_time = models.DateTimeField(null=True, blank = True)
  end_time = models.DateTimeField(null=True, blank = True)
  task = models.TextField(null=True, blank = True)
  task_type = models.IntegerField(default=0)
  attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=True)
  ip = models.TextField(null=True, blank = True)
  os = models.TextField(null=True, blank = True)
  browser = models.TextField(null=True, blank = True)

class Skill(models.Model):
  name = models.CharField(max_length=50, unique=True)
  def __str__(self):
      return self.name

class Note(models.Model):
  content = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  STATUS_CHOICES = (
        ('simple', 'Simple Notes'),
        ('interview', 'Interview Notes'),
    )
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='simple')
  def __str__(self):
      return f"Note {self.content}"

class HiringStatus(models.Model):
  status = models.CharField(max_length=100)
  def __str__(self):
      return self.status

class HiringRecord(models.Model):
  full_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=20)
  address = models.TextField()
  birth_date = models.DateField(null=True, blank=True, verbose_name='Birth Date')
  last_education = models.CharField(max_length=100, null=True, blank=True, verbose_name='Last Education')
  past_experience = models.TextField(null=True, blank=True, verbose_name='Past work experience')
  linkedin_url = models.CharField(max_length=100, null=True, blank=True, verbose_name='LinkedIn Profile URL')
  tiktok_url = models.CharField(max_length=100, null=True, blank=True, verbose_name='TikTok Profile URL')
  fb_url = models.CharField(max_length=100, null=True, blank=True, verbose_name='Facebook Profile URL')
  insta_url = models.CharField(max_length=100, null=True, blank=True, verbose_name='Instagram Profile URL')
  myers_briggs = models.FileField(upload_to='test_results/', null=True, blank=True, verbose_name='Myers Briggs Test')
  typing_test = models.FileField(upload_to='test_results/', null=True, blank=True, verbose_name='Typing Test')
  grammar_test = models.FileField(upload_to='test_results/', null=True, blank=True, verbose_name='Grammar Level Test')
  personality_test = models.FileField(upload_to='test_results/', null=True, blank=True, verbose_name='Similar Minds Personality Test')
  skills = models.ManyToManyField(Skill)
  resume = models.FileField(upload_to='resumes/')
  notes = models.ManyToManyField(Note, blank=True)
  status = models.ForeignKey(HiringStatus, on_delete=models.CASCADE, null=True)

  def __str__(self):
      return self.full_name






