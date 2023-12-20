import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from datetime import datetime
from .models import Attendance,Breaks,Tasks
from django.contrib import messages 
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import pytz
from datetime import timedelta
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.models import User
from user_agents import parse
import datetime
from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice
# Create your views here.
def main(request):
    start = ''
    end = ''
    st_orig = ''
    end_orig = ''
    total_break_time = 0
    my_tasks = 0
    latest_task = ''
    break_yes = None
    
    if not request.user.is_authenticated:
        # messages.success(request,"Please login!")
        return redirect('/login/')
    else:
        today_date = timezone.now().date()
        username = request.user
        today_atten = Attendance.objects.filter(date=timezone.now().date(), user_id=username.id).first()

        curr_date = datetime.datetime.now().date()
        start_of_week = curr_date - timedelta(days=curr_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Query to retrieve records for the current week
        current_week = Attendance.objects.filter(
            Q(date__gte=start_of_week) &
            Q(date__lte=end_of_week)
        ).filter(user_id=username.id)
        current_date = datetime.datetime.now()
        # Calculate the start and end date of the last week
        end_date_of_last_week = current_date - timedelta(days=current_date.weekday() + 1)
        start_date_of_last_week = end_date_of_last_week - timedelta(days=6)

        weekly_atten = Attendance.objects.filter(
            Q(date__gte=start_date_of_last_week) &
            Q(date__lte=end_date_of_last_week)
        ).filter(user_id=username.id)
        # today_atten.delete()
        if today_atten is not None:
            my_breaks = Tasks.objects.filter(attendance_id=today_atten.id,task_type=0).all()
            my_tasks = Tasks.objects.filter(attendance_id=today_atten.id).all().order_by('id')
            la_task = Tasks.objects.filter(attendance_id=today_atten.id,task_type=1).last()
            latest_task = la_task.task
            latest_break = Tasks.objects.filter(attendance_id=today_atten.id).last()
            if latest_break.task_type == 0 and latest_break.end_time == None:
                latest_task = ''
                break_yes = 1
            start_time = today_atten.start_time
            my_zone = start_time.astimezone(pytz.timezone('Asia/Karachi'))
            start = (my_zone.strftime('%I:%M %p'))
            st_orig = start_time.strftime('%H:%M:%S')
            if my_breaks is not None:
                for item in my_breaks:
                    if item.end_time is not None:
                        if item.task_type == 0:
                            st_time = item.start_time
                            en_time = item.end_time
                            break_time = en_time - st_time
                            total_break_time += break_time.total_seconds()
            if today_atten.end_time is not None:
                end_time = today_atten.end_time
                my_zone = end_time.astimezone(pytz.timezone('Asia/Karachi'))
                end = (my_zone.strftime('%I:%M %p'))
                end_orig = end_time.strftime('%H:%M:%S')
                
    return render(request, 'index.html',{'username': username,'today_atten':today_atten,'start':start,'end':end,'st_orig':st_orig,'end_orig':end_orig,'total_break_time':total_break_time,'my_tasks':my_tasks,'latest_task':latest_task,'break_yes':break_yes,'today_date':today_date,'weekly_atten':weekly_atten,'current_week':current_week})
      
def main1(request):
    start = ''
    end = ''
    st_orig = ''
    end_orig = ''
    total_break_time = 0
    my_tasks = 0
    latest_task = ''
    break_yes = None
    
    if not request.user.is_authenticated:
        # messages.success(request,"Please login!")
        return redirect('/login/')
    else:
        today_date = timezone.now().date()
        username = request.user
        today_atten = Attendance.objects.filter(date=timezone.now().date(), user_id=username.id).first()

        curr_date = timezone.now().date()
        start_of_week = curr_date - timedelta(days=curr_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Query to retrieve records for the current week
        current_week = Attendance.objects.filter(
            Q(date__gte=start_of_week) &
            Q(date__lte=end_of_week)
        ).filter(user_id=username.id)
        current_date = datetime.datetime.now()
        # Calculate the start and end date of the last week
        end_date_of_last_week = current_date - timedelta(days=current_date.weekday() + 1)
        start_date_of_last_week = end_date_of_last_week - timedelta(days=6)

        weekly_atten = Attendance.objects.filter(
            Q(date__gte=start_date_of_last_week) &
            Q(date__lte=end_date_of_last_week)
        ).filter(user_id=username.id)
        # today_atten.delete()
        if today_atten is not None:
            my_breaks = Tasks.objects.filter(attendance_id=today_atten.id,task_type=0).all()
            my_tasks = Tasks.objects.filter(attendance_id=today_atten.id).all().order_by('id')
            la_task = Tasks.objects.filter(attendance_id=today_atten.id,task_type=1).last()
            latest_task = la_task.task
            latest_break = Tasks.objects.filter(attendance_id=today_atten.id).last()
            if latest_break.task_type == 0 and latest_break.end_time == None:
                latest_task = ''
                break_yes = 1
            start_time = today_atten.start_time
            my_zone = start_time.astimezone(pytz.timezone('Asia/Karachi'))
            start = (my_zone.strftime('%I:%M %p'))
            st_orig = start_time.strftime('%H:%M:%S')
            if my_breaks is not None:
                for item in my_breaks:
                    if item.end_time is not None:
                        if item.task_type == 0:
                            st_time = item.start_time
                            en_time = item.end_time
                            break_time = en_time - st_time
                            total_break_time += break_time.total_seconds()
            if today_atten.end_time is not None:
                end_time = today_atten.end_time
                my_zone = end_time.astimezone(pytz.timezone('Asia/Karachi'))
                end = (my_zone.strftime('%I:%M %p'))
                end_orig = end_time.strftime('%H:%M:%S')
                
    return render(request, 'index1.html',{'username': username,'today_atten':today_atten,'start':start,'end':end,'st_orig':st_orig,'end_orig':end_orig,'total_break_time':total_break_time,'my_tasks':my_tasks,'latest_task':latest_task,'break_yes':break_yes,'today_date':today_date,'weekly_atten':weekly_atten,'current_week':current_week})
      
    # return HttpResponse(current_week)

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('main')
            elif user is not None:
                login(request, user)
                return redirect('main')
            else:
                msg = 'Please enter the correct username and password for a employee account. Note that both fields may be case-sensitive.'
                return render(request, 'login.html', {'form': form, 'msg': msg})
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def startAtten(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
    os = user_agent.os.family
    browser = user_agent.browser.family
  
    res = {'error': True, 'warn_msg': "Task field can't be empty."}
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        username = request.user
        date = timezone.now().date()
        start_time = timezone.now()
        task = request.POST.get('task', False)
        task_type = request.POST.get('task_type', False)
        started = request.POST.get('started', False)
        update_task = request.POST.get('update_task', False)
        ended = request.POST.get('ended', False)
        mybreak = request.POST.get('break', False)
        back = request.POST.get('back', False)
        ErrorF = {'error': False, "msg": ""}
        if username and start_time and date: 
            
            today_atten = Attendance.objects.filter(date=timezone.now().date(), user_id=username.id).first()
            if today_atten is not None:
                if not ErrorF['error']:
                    if today_atten is not None:
                        if update_task and task:
                            old_task = Tasks.objects.filter(attendance_id=today_atten.id,task_type=1).last()
                            old_task.task = task
                            old_task.ip = ip
                            old_task.browser = browser
                            old_task.os = os
                            old_task.save()
                            res = {'error': False, 'msg': "Task Updated Successfully."}
                        if started and task:
                            latest_break = Tasks.objects.filter(attendance_id=today_atten.id).last()
                            if latest_break.task_type == 0 and latest_break.end_time == None:
                                res = {'error': True, 'warn_msg': "Please Click Back To Task!"}
                            else:
                                Attendance.objects.filter(id=today_atten.id).update(task=task, end_time=None)
                                old_task = Tasks.objects.filter(attendance_id=today_atten.id,task_type=1).last()
                                old_task.end_time = start_time
                                old_task.ip = ip
                                old_task.browser = browser
                                old_task.os = os
                                old_task.save()
                                task = Tasks.objects.create(attendance_id=today_atten.id, start_time=start_time, task=task,task_type=task_type)
                                task.ip = ip
                                task.browser = browser
                                task.os = os
                                task.save()
                                res = {'error': False, 'msg': "Task Added Successfully."}
                        if mybreak:
                            Attendance.objects.filter(id=today_atten.id).update(task=task,end_time=start_time)
                            try:
                                check_break = Tasks.objects.filter(attendance_id=today_atten.id,end_time=None,task_type=0).last()
                            except ObjectDoesNotExist:
                                check_break = None
                            if check_break is not None:
                                res = {'error': True, 'warn_msg': "You have already addedd break!"}
                            else:
                                try:
                                    old_task = Tasks.objects.filter(attendance_id=today_atten.id).last()
                                    old_task.end_time = start_time
                                    old_task.ip = ip
                                    old_task.browser = browser
                                    old_task.os = os
                                    old_task.save()
                                except ObjectDoesNotExist:
                                    old_task = None
                                task = Tasks.objects.create(attendance_id=today_atten.id, start_time=start_time, task=task,task_type=task_type)
                                task.ip = ip
                                task.browser = browser
                                task.os = os
                                task.save()
                                res = {'error': False, 'msg': "Break Added Successfully."}
                        if back:
                            latest_break = Tasks.objects.filter(attendance_id=today_atten.id,end_time=None,task_type=0).last()
                            if latest_break is not None:
                                Attendance.objects.filter(id=today_atten.id).update(task=task,end_time=None)
                                old_task = Tasks.objects.filter(id=latest_break.id).update(end_time=start_time,  ip=ip, os=os, browser=browser)
                                pre_task = Tasks.objects.filter(attendance_id=today_atten.id,task_type=1).last()
                                task = Tasks.objects.create(attendance_id=today_atten.id, start_time=start_time, task=pre_task.task,task_type=1, ip=ip, os=os, browser=browser)
                                res = {'error': False, 'msg': "Back Added Successfully."}
                            else:
                                res = {'error': False, 'warn_msg': "Please add break first!"}
                        if ended:
                            Attendance.objects.filter(id=today_atten.id).update(end_time=start_time,ended=ended,  ip_end=ip, os_end=os, browser_end=browser)
                            latest_task = Tasks.objects.filter(attendance_id=today_atten.id).last()
                            latest_task.end_time = start_time
                            latest_task.ip = ip
                            latest_task.browser = browser
                            latest_task.os = os
                            latest_task.save()
                            res = {'error': False, 'msg': "Time Ended Successfully."}
                    else:
                        res = {'error': False, 'warn_msg': "Today Time Already Recorded."}
                elif ErrorF['error']:
                    res = ErrorF
                else:
                    res = {'error': True, 'warn_msg': "Please enter task."}
            elif started:
                if task:
                    if not ErrorF['error']:
                        attendance = Attendance.objects.create(user_id=username.id, date=date, start_time=start_time, task=task)
                        attendance.ip_start = ip
                        attendance.browser_start = browser
                        attendance.os_start = os
                        attendance.save()
                        task = Tasks.objects.create(attendance_id=attendance.id, start_time=start_time, task=task,task_type=task_type)
                        task.ip = ip
                        task.browser = browser
                        task.os = os
                        task.save()
                        res = {'error': False, 'msg': "Time Started Successfully."}
                    elif ErrorF['error']:
                        res = ErrorF
                    else:
                        res = {'error': True, 'warn_msg': "Form not submitted. Try with a refresh."}
            else:
               res = {'error': True, 'warn_msg': "Please Start Your Time!"} 
        else:
            res = {'error': True, 'warn_msg': "Fill all required fields."}
        return JsonResponse(res)

def allAttendance(request):
    username = request.user
    all_attendance  = Attendance.objects.filter( user_id=username.id).all().order_by('id')
    out = []
    for attendance in all_attendance:
        all_tasks  = Tasks.objects.filter(attendance_id=attendance.id).all().order_by('id')
        for task in all_tasks:
            start_time = task.start_time
            my_zone = start_time.astimezone(pytz.timezone('Asia/Karachi'))
            start = (my_zone.strftime('%m/%d/%Y, %H:%M:%S'))
            if task.end_time is not None:
                end_time = task.end_time
                my_zone = end_time.astimezone(pytz.timezone('Asia/Karachi'))
                end = (my_zone.strftime('%m/%d/%Y, %H:%M:%S'))
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
                    'total':total,
                    'title':task_detail,
                    'color':color,
                })
    return JsonResponse(out, safe=False)
def userAttendance(request):
    username = request.user
    all_attendance  = Attendance.objects.filter( user_id=username.id).all().order_by('id')
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
                out.append({
                    'id':task.id,
                    'start':start,
                    'end':end,
                    'total':total,
                    'title':task.task,
                    'color':color,
                })
    return JsonResponse(out, safe=False)

def admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'admin.html')
    else:
        return redirect('employee')

def employee(request):
    if request.user.is_authenticated:
        return render(request,'employee.html')
    else:
        return redirect('login_view')
    
def allUserAttendance(request):
    all_attendance  = Attendance.objects.all().order_by('id')
    out = []
    total_break_time = 0
    for attendance in all_attendance:
        user = User.objects.filter(id=attendance.user_id).first()
        start_time = attendance.start_time
        my_zone = start_time.astimezone(pytz.timezone('Asia/Karachi'))
        start = (my_zone.strftime('%Y-%m-%dT%H:%M:%S'))
        end_time = attendance.end_time
        if end_time is not None:
            end_time = end_time
        else:
            end_time = datetime.datetime.now()
        my_breaks = Tasks.objects.filter(attendance_id=attendance.id,task_type=0).all()
        if my_breaks is not None:
            for item in my_breaks:
                if item.end_time is not None:
                    if item.task_type == 0:
                        st_time = item.start_time
                        en_time = item.end_time
                        break_time = en_time - st_time
                        total_break_time += break_time.total_seconds()
        my_zone = end_time.astimezone(pytz.timezone('Asia/Karachi'))
        end = (my_zone.strftime('%Y-%m-%dT%H:%M:%S'))
        weekday = end_time.weekday()
        if weekday == 0:
            color = '#00D506'
        elif weekday == 1:
            color = '#8AFF33'
        elif weekday == 2:
            color = '#7CF48C'
        elif weekday == 3:
            color = '#69FFEF'
        elif weekday == 4:
            color = '#55C4FF'
        # Icons added 
        if attendance.os_start == 'Windows':
            username = "🖥️" + user.username
        elif attendance.os_start == 'Andriod' or attendance.os_start == 'ios':
            username = "📱" + user.username
        else:
            username = user.username
        out.append({
            'id':attendance.id,
            'start':start,
            'end':end,
            'title':username,
            'color':color,
            # 'url':total_break_time,
        })
    return JsonResponse(out, safe=False)

def getDashboard(request):
    
    # url = "https://onesignal.com/api/v1/notifications"

    # payload = {
    #     "app_id": "4884e1b9-2418-48df-af91-bab9737ea242",  
    #     "included_segments": ["Active Subscriptions"],
    #     "contents": {
    #         "en": "User Start Attendance",
    #         "es": "Spanish Message"
    #     }
    # }

    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Basic NmE1OTJiMTgtYzJmNy00MjU0LTg2NDItZjQzMDY0OWVmNzNm"
    # }

    # response = requests.post(url, json=payload, headers=headers)
    # return JsonResponse(response.text, safe=False)
    # print(response.text)
    total = User.objects.filter(is_staff=True, is_superuser=False).count()
    active = Attendance.objects.filter(date=timezone.now().date()).count()
    absent = total - active
    res = {'total': total, 'active': active, 'absent': absent}
    return JsonResponse(res)

def getTasks(request):
    out = []
    atten_id = request.POST.get('atten_id', False)
    all_tasks = Tasks.objects.filter(attendance_id=atten_id).all().order_by('id')
    for task in all_tasks:
        start_time = task.start_time
        my_zone = start_time.astimezone(pytz.timezone('Asia/Karachi'))
        start = (my_zone.strftime('%m/%d/%Y, %H:%M:%S'))
        if task is not None:
            if task.end_time is not None:
                end_time = task.end_time
            else:
                end_time = datetime.datetime.now(timezone.utc)
            my_zone = end_time.astimezone(pytz.timezone('Asia/Karachi'))
            end = (my_zone.strftime('%m/%d/%Y, %H:%M:%S'))
            total_time = end_time - start_time
            total = total_time.total_seconds()
            if task.task_type == 0:
                mytask = 'BREAK'
            else:
                mytask = 'TASK'
            if task.os == 'Windows':
                device  = '🖥️\n' + 'IP: ' + task.ip + '\n' + 'Browser: ' + task.browser
            elif task.os == 'Andriod' or task.os == 'ios':
                device = '📱 \n' + 'IP: ' + task.ip + '\n' + 'Browser: ' + task.browser
            else:
                device = ""
            out.append({
                'id':task.id,
                'start':start,
                'end':end,
                'total':total,
                'title':task.task,
                'type':mytask,
                'device':device,
            })
    return JsonResponse(out, safe=False)

# Firebase integration
def send(request):
    message_obj = Message(
        data={
            "title" : "Talha",
            "body" : "great match!",
        },
    )
    device = FCMDevice.objects.all().first()
    device.send_message(message_obj)

