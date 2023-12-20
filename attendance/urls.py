from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static 
#Django admin header customization
admin.site.site_header = "NVT Attendance System"
admin.site.site_title = "NVT Attendance System"
admin.site.index_title = "NVT Attendance System"
urlpatterns = [
    path('', views.main, name='main'),
    path('index1/', views.main1, name='main1'),
    path('login/', views.login_view, name='login_view'),
    path('start/', views.startAtten, name='startAtten'),
    path('all_attendance/', views.allAttendance, name='allAttendance'),
    path('user_ttendance/', views.userAttendance, name='userAttendance'),
    path('get_dashboard/', views.getDashboard, name='getDashboard'),
    path('all_users_attendance/', views.allUserAttendance, name='allUserAttendance'),
    path('get_tasks/', views.getTasks, name='getTasks'),
    path('admin_panel/', views.admin, name='adminpage'),
    path('employee_panel/', views.employee, name='employee'),
]
if settings.DEBUG:     
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)