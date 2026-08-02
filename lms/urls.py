from django.urls import path
from . import views
from .views import user_logout, CustomLoginView

urlpatterns = [
    path('',views.home,name = 'home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('courses/', views.courses, name='courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('study-materials/', views.study_materials, name='study_materials'),
    path('assignments/', views.assignments, name='assignments'),
    path(
    'submit-assignment/<int:assignment_id>/',
    views.submit_assignment,
    name='submit_assignment'
),
    path('quizzes/', views.quizzes, name='quizzes'),
    path(
    'take-quiz/<int:quiz_id>/',
    views.take_quiz,
    name='take_quiz'
),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]   