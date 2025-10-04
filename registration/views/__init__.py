# สำหรับรวบรวมทุก View
from .student import *

class HomeView(View):
    def get(self, request):
        user_role = request.session.get("user_role", "")

        if user_role=="Student":
            return redirect("login_view")

        elif user_role=="Staff":
            return redirect("staff_home_view")
        
        return redirect("login_view")
    