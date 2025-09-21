# myapp/middleware.py
from django.shortcuts import redirect

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # รายการ URL ที่ไม่ต้อง login
        excluded_paths = ['/login/', '/static/']

        if not request.session.get('user_email') and request.path not in excluded_paths:
            return redirect('/login/')

        response = self.get_response(request)
        return response
