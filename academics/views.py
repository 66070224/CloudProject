from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views import View
from . import forms
from . import models
from django.db import transaction

# Create your views here.
class ManageCourseView(View):
    def get(self, request):
        invalid = request.session.pop("invalid", False)
        courses = models.Course.objects.all()
        form = forms.CourseForm(invalid) if invalid else forms.CourseForm()

        return render(request, "course.html", context={
            "courses": courses, "is_invalid": invalid, "form": form
        })
    def post(self, request):
        form = forms.CourseForm(request.POST)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_course_view')
                
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('manage_course_view')


class EditCourseView(View):
    def get(self, request, course_code):
        invalid = request.session.pop("invalid", False)
        course = models.Course.objects.get(pk=course_code)
        form = forms.CourseForm(invalid, instance=course) if invalid else forms.CourseForm(instance=course)

        return render(request, "edit_course.html", context={
            "form": form
        })
    def post(self, request, course_code):
        course = models.Course.objects.get(pk=course_code)
        form = forms.CourseForm(request.POST, instance=course)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_course_view')
                
                print(f"Invalid form: {form.errors}")
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('edit_course_view', id=id)


class ManageSectionView(View):
    def get(self, request):
        invalid = request.session.pop("invalid", False)
        sections = models.CourseSection.objects.all()
        form = forms.SectionForm(invalid) if invalid else forms.SectionForm()

        return render(request, "section.html", context={
            "sections": sections, "is_invalid": invalid, "form": form
        })
    def post(self, request):
        form = forms.SectionForm(request.POST)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_section_view')
                
                print(f"Invalid form: {form.errors}")
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('manage_section_view')
    def get_professors(request):
        course_id = request.GET.get("course_id")
        data = []
        if course_id:
            try:
                course = models.Course.objects.get(pk=course_id)
                professors = models.Professor.objects.filter(department=course.department)
                data = [{"id": p.id, "name": f"{p.first_name} {p.last_name}"} for p in professors]
            except models.Course.DoesNotExist:
                pass
        return JsonResponse(data, safe=False)

    
class EditSectionView(View):
    def get(self, request, id):
        invalid = request.session.pop("invalid", False)
        section = models.CourseSection.objects.get(pk=id)
        form = forms.SectionForm(invalid, instance=section) if invalid else forms.SectionForm(instance=section)

        return render(request, "edit_section.html", context={
            "form": form
        })
    def post(self, request, id):
        section = models.CourseSection.objects.get(pk=id)
        form = forms.SectionForm(request.POST, instance=section)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_section_view')
                
                print(f"Invalid form: {form.errors}")
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('edit_section_view', id=id)

class ManageDepartmentView(View):
    def get(self, request):
        invalid = request.session.pop("invalid", False)
        departments = models.Department.objects.all()
        form = forms.DepartmentForm(invalid) if invalid else forms.DepartmentForm()

        return render(request, "department.html", context={
            "departments": departments, "is_invalid": invalid, "form": form
        })
    def post(self, request):
        form = forms.DepartmentForm(request.POST)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_department_view')
                
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('manage_department_view')
    
class EditDepartmentView(View):
    def get(self, request, id):
        invalid = request.session.pop("invalid", False)
        department = models.Department.objects.get(pk=id)
        form = forms.DepartmentForm(invalid, instance=department) if invalid else forms.DepartmentForm(instance=department)

        return render(request, "edit_department.html", context={
            "form": form
        })
    def post(self, request, id):
        department = models.Department.objects.get(pk=id)
        form = forms.DepartmentForm(request.POST, instance=department)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_department_view')
                
                print(f"Invalid form: {form.errors}")
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('edit_department_view', id=id)


class ManageProfessorView(View):
    def get(self, request):
        invalid = request.session.pop("invalid", False)
        professors = models.Professor.objects.all()
        form = forms.ProfessorForm(invalid) if invalid else forms.ProfessorForm()

        return render(request, "professor.html", context={
            "professors": professors, "is_invalid": invalid, "form": form
        })
    def post(self, request):
        form = forms.ProfessorForm(request.POST)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_professor_view')
                
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('manage_professor_view')
    
class EditProfessorView(View):
    def get(self, request, id):
        invalid = request.session.pop("invalid", False)
        professor = models.Professor.objects.get(pk=id)
        form = forms.ProfessorForm(invalid, instance=professor) if invalid else forms.ProfessorForm(instance=professor)

        return render(request, "edit_professor.html", context={
            "form": form
        })
    def post(self, request, id):
        professor = models.Professor.objects.get(pk=id)
        form = forms.ProfessorForm(request.POST, instance=professor)

        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()

                    return redirect('manage_professor_view')
                
                print(f"Invalid form: {form.errors}")
                raise transaction.TransactionManagementError("Error")
        except Exception as e:
            print(f"Error {e}")
            request.session["invalid"] = request.POST

            return redirect('edit_professor_view', id=id)