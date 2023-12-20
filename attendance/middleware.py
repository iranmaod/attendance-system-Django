class SuperuserCustomIndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_superuser:
            from django.contrib import admin
            admin.site.index_template = 'admin/admin_dashboard.html'
        elif request.user.is_staff:
            from django.contrib import admin
            admin.site.index_template = 'admin/employee_dashboard.html'
        return self.get_response(request)