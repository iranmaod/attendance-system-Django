from django.contrib import admin
from datetime import datetime, timedelta
from .models import Attendance,Tasks, HiringRecord, Note, Skill, HiringStatus
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.urls import path
from django.utils import timezone
import pytz
# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username','get_start_time','task','get_end_time','get_total_time')  # Display user_id and username in the admin list view
    actions = ['get_username_action'] 

    # Define a custom admin action to retrieve the username
    def get_username_action(self, request, queryset):
        for nvt_user in queryset:
            user_id = nvt_user.user_id  # Assuming 'user_id' is a field in the StaffAdmin model
            try:
                user = User.objects.get(id=user_id)
                self.message_user(request, f'User ID: {user_id} - Username: {user.username}')
            except User.DoesNotExist:
                self.message_user(request, f'User ID: {user_id} - User not found')

    get_username_action.short_description = "Get Username"  # Action description in the admin interface

    # Define a method to display the username in the admin list view
    def get_username(self, obj):
        if obj.user_id:
            try:
                user = User.objects.get(id=obj.user_id)
                return user.username
            except User.DoesNotExist:
                return "User not found"
        return "N/A"
    def get_start_time(self, obj):
        if obj.start_time:
            start_time = obj.start_time + timedelta(hours=5)
            return start_time
    def get_end_time(self, obj):
        if obj.end_time:
            start_time = obj.end_time + timedelta(hours=5)
            return start_time
    def get_total_time(self, obj):
        if obj.end_time:
            total_break_time = 0
            my_breaks = Tasks.objects.filter(attendance_id=obj.id,task_type=0).all()
            if my_breaks is not None:
                for item in my_breaks:
                    if item.end_time is not None:
                        br_time = item.start_time
                        bk_time = item.end_time
                        break_time = bk_time - br_time
                        total_break_time += break_time.total_seconds()
            starttime = obj.start_time
            endtime = obj.end_time
            start = starttime.timestamp()
            end = endtime.timestamp()
            total_time = int(end - start - total_break_time)
            hours = total_time // 3600
            remaining_seconds = total_time % 3600
            minutes = remaining_seconds // 60
            time_spend = str(hours)+" hours " + str(minutes) + " minutes"
            return time_spend

    get_username.short_description = "Username" 
    get_start_time.short_description = "Start Time" 
    get_end_time.short_description = "End Time" 
    get_total_time.short_description = "Total Time" 

class UserDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "admin.view_user"
    template_name = "admin/users/detail.html"
    model = User
    def get_context_data(self, **kwargs):
        user_id = self.kwargs.get('pk')
        user_tasks = ''
        today_atten = Attendance.objects.filter(date=timezone.now().date(),user_id=user_id).first()
        if today_atten is not None:
            user_tasks = Tasks.objects.filter(attendance_id=today_atten.id).all().order_by('id')
        #Get all tasks in calendar view
        all_attendance  = Attendance.objects.filter( user_id=user_id).all().order_by('id')
        out = []
        for attendance in all_attendance:
            all_tasks  = Tasks.objects.filter(attendance_id=attendance.id).all().order_by('id')
            for task in all_tasks:
                start_time = task.start_time
                my_zone = start_time.astimezone(pytz.timezone('Asia/Karachi'))
                start = (my_zone.strftime('%Y-%m-%dT%H:%M:%S'))
                if task.end_time is not None:
                    end_time = task.end_time
                    my_zone = end_time.astimezone(pytz.timezone('Asia/Karachi'))
                    end = (my_zone.strftime('%Y-%m-%dT%H:%M:%S'))
                    total_time = end_time - start_time
                    total = total_time.total_seconds()
                    weekday = end_time.weekday()
                    if task.task_type == 0:
                        color = '#DC3545'
                    elif weekday == 0:
                        color = '#00D506'
                    elif weekday == 1:
                        color = '#8AFF33'
                    elif weekday == 2:
                        color = '#7CF48C'
                    elif weekday == 3:
                        color = '#69FFEF'
                    elif weekday == 4:
                        color = '#55C4FF'
                    if task.os == 'Windows':
                        task_detail = "🖥️" + task.task
                    elif task.os == 'Andriod' or task.os == 'ios':
                        task_detail = "📱" + task.task
                    else:
                        task_detail = task.task
                    out.append({
                        'id':task.id,
                        'start':start,
                        'end':end,
                        'title':task_detail,
                        'color':color,
                    })
    
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
            "user_tasks": user_tasks,
            "all_tasks": out,
        }


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'user_details')

    def get_urls(self):
        return [
            path(
                "<pk>/detail",
                self.admin_site.admin_view(UserDetailView.as_view()),
                name=f"user_details",
            ),
            *super().get_urls(),
        ]

    def user_details(self, obj):
        url = reverse("admin:user_details", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')


admin.site.register(Attendance, MemberAdmin)

class allRecords(admin.ModelAdmin):
    list_display = ('full_name','email','phone')
admin.site.register(HiringRecord, allRecords)
# admin.site.register(HiringStatus)
admin.site.register(Skill)
admin.site.register(Note)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.site_header = 'Custom Admin Dashboard'