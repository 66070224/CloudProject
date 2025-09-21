from .models import Student

def current_user(request):
    user = None
    user_email = request.session.get('user_email')
    user_role = request.session.get('user_role', "")
    is_login = False
    if user_email:
        is_login = True
        try:
            user = Student.objects.get(email=user_email)
        except Student.DoesNotExist:
            pass
        
    return {'user': user, 'role': user_role, "is_login": is_login}
