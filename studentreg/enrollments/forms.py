from django.forms import ModelForm
from enrollments.models import Grade

class GradeForm(ModelForm):
    class Meta():
        model=Grade
        fields=['score1', 'score2', 'score3', 'score4']