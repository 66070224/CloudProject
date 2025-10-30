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
from departments.models import Department

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

        if not (request.user.is_registra or request.user.is_professor):
            return redirect(reverse("home"))

        code = request.GET.get("code", "")
        name = request.GET.get("name", "")
        department_select = request.GET.get("department_select", "")
        year = request.GET.get("year", "")
        term = request.GET.get("term", "")

        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            courses = Course.objects.filter(department__faculty=registra.faculty)
            departments = Department.objects.filter(faculty=registra.faculty)
        elif request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            courses = Course.objects.filter(professors=professor)
            departments = Department.objects.filter(faculty=professor.faculty)

        if code and code != "None":
            courses = courses.filter(code__icontains=code)
        if name and name != "None":
            courses = courses.filter(name__icontains=name)
        if department_select and department_select != "None":
            courses = courses.filter(department__name=department_select)
        if year and year != "None":
            try:
                courses = courses.filter(year=int(year))
            except Exception:
                pass
        if term and term != "None":
            try:
                courses = courses.filter(term=int(term))
            except Exception:
                pass


        return render(request, "courses/list/course.html", {"courses": courses, "code": code, "name": name, "department_select": department_select, "year": year, "term": term, "departments": departments })
    
class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, code):

        if not (request.user.is_registra or request.user.is_professor):
            return redirect(reverse("home"))
        
        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            faculty = registra.faculty
            course = Course.objects.get(code=code, faculty=faculty)

        if request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            course = Course.objects.get(code=code, professors=professor)
        
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

        if not (request.user.is_registra or request.user.is_professor):
            return redirect(reverse("home"))

        code = request.GET.get("code", "")
        section_number = request.GET.get("section_number", "")

        if request.user.is_registra:
            registra = Registra.objects.get(user=request.user)
            sections = Section.objects.filter(course__department__faculty=registra.faculty)
        elif request.user.is_professor:
            professor = Professor.objects.get(user=request.user)
            sections = Section.objects.filter(course__professors=professor)

        if code and code != "None":
            sections = sections.filter(course__code__icontains=code)
        if section_number and section_number != "None":
            sections = sections.filter(number__icontains=section_number)

        return render(request, "courses/list/section.html", {"sections": sections, "code": code, "section_number": section_number})
    
class SectionDetailView(LoginRequiredMixin, View):
    def get(self, request, id):

        if not (request.user.is_registra or request.user.is_professor):
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

        types = ["LEC", "LAB"]
        code = request.GET.get("code", "")
        section_number = request.GET.get("section_number", "")
        type = request.GET.get("type", "")

        registra = Registra.objects.get(user_id=request.user.id)
        classes = Class.objects.filter(section__course__department__faculty=registra.faculty)

        if code and code != "None":
            classes = classes.filter(section__course__code__icontains=code)
        if section_number and section_number != "None":
            classes = classes.filter(section__number__icontains=section_number)
        if type and type != "None":
            classes = classes.filter(type=type)
        

        return render(request, "courses/list/class.html", {"classes": classes, "types": types, "code": code, "section_number": section_number, "type": type})

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
    
class DeleteAPI(LoginRequiredMixin, APIView):

    def get(self, request, type, id):

        if not request.user.is_registra:
            return redirect(reverse("home"))

        try:
            if type == "course":
                course = Course.objects.get(code=id)
                course.delete()
                return redirect(request.META['HTTP_REFERER'])
            elif type == "section":
                section = Section.objects.get(id=id)
                section.delete()
                return redirect(request.META['HTTP_REFERER'])
            elif type == "class":
                aclass = Class.objects.get(id=id)
                aclass.delete()
                return redirect(request.META['HTTP_REFERER'])
        except Class.DoesNotExist:
            return Response({
                "text": "ไม่พบข้อมูลที่ต้องการลบ"
            }, status=404)
        except IntegrityError:
            return Response({
                "text": "ไม่สามารถลบข้อมูลได้ เนื่องจากมีการใช้งานอยู่"
            }, status=400)
