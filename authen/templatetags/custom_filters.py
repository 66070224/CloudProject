from django import template

register = template.Library()

@register.filter
def is_student(role):
    return role == "Student"

@register.filter
def is_staff(role):
    return role == "Staff"