from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(StudyMaterial)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizResult)
admin.site.register(Profile)