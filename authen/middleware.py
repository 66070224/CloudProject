# myapp/middleware.py
from django.shortcuts import redirect
from django.http import JsonResponse

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        excluded_admin_paths = ['/admin/', '/admin/login/', '/admin/logout/']

        # ไม่บล็อก static และ admin
        if path.startswith('/static/') or path in excluded_admin_paths or path.startswith('/admin/'):
            return self.get_response(request)

        # ตรวจสอบ login
        if not request.session.get('user_email') and not path.startswith('/auth/'):
            return redirect('login_view')

        # Staff block student paths
        elif request.session.get('user_role') == "Staff" and (
            path.startswith('/student/') or path in ['/login/', '/change_password/', '/registration/']
        ):
            return redirect('staff_home_view')

        # Student block staff paths
        elif request.session.get('user_role') == "Student" and (
            path.startswith('/staff/') or path in ['/login/', '/change_password/', '/registration/']
        ):
            return JsonResponse({'message': 'You are student.'})

        return self.get_response(request)
