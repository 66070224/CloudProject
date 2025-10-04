from users.models import Student

def current_user(request):
    user_email = request.session.get('user_email')
    user_role = request.session.get('user_role', "")
    is_login = False
    if user_email:
        is_login = True
        
    return {'role': user_role, "is_login": is_login}
