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

# Create your views here.
class CourseDetailAPI(APIView):

    def get_object(self, code):
        try:
            return Course.objects.get(code=code)
        except Course.DoesNotExist:
            return Http404

    def get(self, request, code):
        course = self.get_object(code)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

class MyCourseView(View):
    def get(self, request):
        professor = Professor.objects.get(user_id=request.user.id)
        courses = Course.objects.filter(professors=professor)
        return render(request, "courses/professor/course.html", {"courses": courses})
    
class RegistraIndexView(View):
    def get(self, request):
        return render(request, "courses/registra/index.html")
    
class RegistraCourseView(View):
    def get(self, request):

        text = request.GET.get("text")
        type = request.GET.get("type")

        registra = Registra.objects.get(user_id=request.user.id)
        courses = Course.objects.filter(department__faculty=registra.faculty)

        if text and type and text != "None":
            if type == "code":
                courses = courses.filter(code=text)
            elif type == "name":
                courses = courses.filter(name=text)
            elif type == "department":
                courses = courses.filter(department__name__icontains=text)
            elif type == "faculty":
                courses = courses.filter(department__faculty__name__icontains=text)
            elif type == "year":
                courses = courses.filter(year=text)
            elif type == "term":
                courses = courses.filter(term=text)

        if text == "None" or text == None:
            text = ""

        return render(request, "courses/registra/list/course.html", {"courses": courses, "text": text, "type": type})
    
class CreateCourseView(View):
    def get(self, request):
        form = CourseForm()
        return render(request, "courses/registra/create/course.html", {"form": form})
    def post(self, request):
        form = CourseForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    form.save_m2m()
                    return redirect(reverse("course_registra_courselist"))
                return render(request, "courses/registra/create/course.html", {"form": form})
        except IntegrityError:
            return render(request, "courses/registra/create/course.html", {"form": form})
    
class EditCourseView(View):
    def get(self, request, id):
        course = Course.objects.get(id=id)
        form = CourseForm(instance=course)
        return render(request, "courses/registra/edit/course.html", {"form": form})
    def post(self, request, id):
        course = Course.objects.get(id=id)
        form = CourseForm(request.POST, instance=course)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    form.save_m2m()
                    return redirect(reverse("course_registra_courselist"))
                return render(request, "courses/registra/edit/course.html", {"form": form})
        except IntegrityError:
            return render(request, "courses/registra/edit/course.html", {"form": form})
    
class RegistraSectionView(View):
    def get(self, request):

        text = request.GET.get("text")
        type = request.GET.get("type")

        registra = Registra.objects.get(user_id=request.user.id)
        sections = Section.objects.filter(course__department__faculty=registra.faculty)

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

        return render(request, "courses/registra/list/section.html", {"sections": sections, "text": text, "type": type})

class CreateSectionView(View):
    def get(self, request):
        form = SectionForm()
        return render(request, "courses/registra/create/section.html", {"form": form})
    def post(self, request):
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_registra_courselist"))
        return render(request, "courses/registra/create/section.html", {"form": form})

class EditSectionView(View):
    def get(self, request, id):
        section = Section.objects.get(id=id)
        form = SectionForm(instance=section)
        return render(request, "courses/registra/edit/section.html", {"form": form})
    def post(self, request, id):
        section = Section.objects.get(id=id)
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_registra_sectionlist"))
        return render(request, "courses/registra/edit/section.html", {"form": form})
    
class RegistraClassView(View):
    def get(self, request):

        text = request.GET.get("text")
        type = request.GET.get("type")

        registra = Registra.objects.get(user_id=request.user.id)
        classes = Class.objects.filter(section__course__department__faculty=registra.faculty)

        if text and type and text != "None":
            pass

        if text == "None" or text == None:
            text = ""

        return render(request, "courses/registra/list/class.html", {"classes": classes, "text": text, "type": type})

class CreateClassView(View):
    def get(self, request):
        form = ClassForm()
        return render(request, "courses/registra/create/class.html", {"form": form})
    def post(self, request):
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_registra_classlist"))
        return render(request, "courses/registra/create/class.html", {"form": form})

class EditClassView(View):
    def get(self, request, id):
        aclass = Class.objects.get(id=id)
        form = ClassForm(instance=aclass)
        return render(request, "courses/registra/edit/class.html", {"form": form})
    def post(self, request, id):
        aclass = Class.objects.get(id=id)
        form = ClassForm(request.POST, instance=aclass)
        if form.is_valid():
            form.save()
            return redirect(reverse("course_registra_classlist"))
        return render(request, "courses/registra/edit/class.html", {"form": form})