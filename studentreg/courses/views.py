from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from courses.models import Course, Section, Class
from django.http import Http404
from courses.serializers import CourseSerializer
from rest_framework.response import Response
from personnels.models import Professor, Registra
from courses.forms import CourseForm, SectionForm, ClassForm
from django.db import transaction, IntegrityError
from enrollments.models import Enroll

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CourseIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "courses/index.html")


#----------------------------------------------------------------------------------------------------------------------------
# COURSE
#----------------------------------------------------------------------------------------------------------------------------
class CourseListView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_registra or request.user.is_professor:
            return redirect(reverse("home"))

        text = request.GET.get("text")
        type = request.GET.get("type")

        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            courses = Course.objects.filter(department__faculty=registra.faculty)
        elif request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            courses = Course.objects.filter(professors=professor)

        if text and type and text != "None":
            if type == "code":
                courses = courses.filter(code=text)
            elif type == "name":
                courses = courses.filter(name=text)
            elif type == "department":
                courses = courses.filter(department__name__icontains=text)
            elif type == "year":
                courses = courses.filter(year=text)
            elif type == "term":
                courses = courses.filter(term=text)

        if text == "None" or text == None:
            text = ""

        return render(request, "courses/list/course.html", {"courses": courses, "text": text, "type": type})
    
class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, code):

        if not request.user.is_registra or request.user.is_professor:
            return redirect(reverse("home"))
        
        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            faculty = registra.faculty

        if request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            faculty = professor.faculty
        
        course = Course.objects.get(code=code, faculty=faculty)
        return render(request, "courses/detail/course.html", {"course": course})

class CreateCourseView(LoginRequiredMixin, View):
    def get(self, request):
        
        if not request.user.is_registra:
            return redirect(reverse("home"))

        form = CourseForm()
        return render(request, "courses/create/course.html", {"form": form})
    def post(self, request):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        form = CourseForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect(reverse("course_course_list"))
                return render(request, "courses/create/course.html", {"form": form})
        except IntegrityError:
            return render(request, "courses/create/course.html", {"form": form})

class EditCourseView(LoginRequiredMixin, View):
    def get(self, request, code):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        course = Course.objects.get(code=code)
        form = CourseForm(instance=course)
        return render(request, "courses/edit/course.html", {"form": form})
    def post(self, request, code):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        course = Course.objects.get(code=code)
        form = CourseForm(request.POST, instance=course)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect(reverse("course_course_list"))
                return render(request, "courses/edit/course.html", {"form": form})
        except IntegrityError:
            return render(request, "courses/edit/course.html", {"form": form})



#----------------------------------------------------------------------------------------------------------------------------
# SECTION
#----------------------------------------------------------------------------------------------------------------------------
class SectionListView(LoginRequiredMixin, View):
    def get(self, request):

        if not request.user.is_registra or request.user.is_professor:
            return redirect(reverse("home"))

        text = request.GET.get("text")
        type = request.GET.get("type")

        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            sections = Section.objects.filter(course__department__faculty=registra.faculty)
        elif request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            sections = Section.objects.filter(course__professors=professor)

        if text and type and text != "None":
            if type == "course":
                sections = sections.filter(course__name__icontains=text)
            elif type == "section":
                try:
                    sections = sections.filter(number=int(text))
                except Exception:
                    pass

        if text == "None" or text == None:
            text = ""

        return render(request, "courses/list/section.html", {"sections": sections, "text": text, "type": type})
    
class SectionDetailView(LoginRequiredMixin, View):
    def get(self, request, id):

        if not request.user.is_registra or request.user.is_professor:
            return redirect(reverse("home"))
        
        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            section = Section.objects.get(course__faculty=registra.faculty, id=id)
        elif request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            section = Section.objects.get(course__professors=professor, id=id)
        enrolls = Enroll.objects.filter(section=section, status="con")
        return render(request, "courses/detail/section.html", {"section": section, "enrolls": enrolls})
    
class CreateSectionView(LoginRequiredMixin, View):
    def get(self, request):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        form = SectionForm()
        return render(request, "courses/create/section.html", {"form": form})
    def post(self, request):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_section_list"))
        return render(request, "courses/create/section.html", {"form": form})
    
class EditSectionView(LoginRequiredMixin, View):
    def get(self, request, id):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        section = Section.objects.get(id=id)
        form = SectionForm(instance=section)
        return render(request, "courses/edit/section.html", {"form": form})
    def post(self, request, id):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        section = Section.objects.get(id=id)
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_section_list"))
        return render(request, "courses/edit/section.html", {"form": form})



#----------------------------------------------------------------------------------------------------------------------------
# CLASS
#----------------------------------------------------------------------------------------------------------------------------
class ClassListView(LoginRequiredMixin, View):
    def get(self, request):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        text = request.GET.get("text")
        type = request.GET.get("type")

        registra = Registra.objects.get(user_id=request.user.id)
        classes = Class.objects.filter(section__course__department__faculty=registra.faculty)

        if text and type and text != "None":
            pass

        if text == "None" or text == None:
            text = ""

        return render(request, "courses/list/class.html", {"classes": classes, "text": text, "type": type})

class CreateClassView(LoginRequiredMixin, View):
    def get(self, request):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        form = ClassForm()
        return render(request, "courses/create/class.html", {"form": form})
    def post(self, request):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_class_list"))
        return render(request, "courses/create/class.html", {"form": form})
    
class EditClassView(LoginRequiredMixin, View):
    def get(self, request, id):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        aclass = Class.objects.get(id=id)
        form = ClassForm(instance=aclass)
        return render(request, "courses/edit/class.html", {"form": form})
    def post(self, request, id):
                
        if not request.user.is_registra:
            return redirect(reverse("home"))

        aclass = Class.objects.get(id=id)
        form = ClassForm(request.POST, instance=aclass)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_class_list"))
        return render(request, "courses/edit/class.html", {"form": form})



#----------------------------------------------------------------------------------------------------------------------------
# API
#----------------------------------------------------------------------------------------------------------------------------
class CourseDetailAPI(LoginRequiredMixin, APIView):

    def get_object(self, code):
        try:
            return Course.objects.get(code=code)
        except Course.DoesNotExist:
            return Http404

    def get(self, request, code):
        course = self.get_object(code)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
