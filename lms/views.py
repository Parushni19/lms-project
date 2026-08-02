from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q

from .models import (
    Course,
    Enrollment,
    StudyMaterial,
    Assignment,
    AssignmentSubmission,
    Quiz,
    Question,
    QuizResult
)

from .forms import AssignmentSubmissionForm


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


class CustomLoginView(LoginView):
    template_name = 'login.html'


def courses(request):
    query = request.GET.get('q')

    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        courses = Course.objects.all()

    return render(
        request,
        'courses.html',
        {'courses': courses}
    )


@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    return redirect('/courses/')


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    )

    return render(
        request,
        'my_courses.html',
        {'enrollments': enrollments}
    )


@login_required
def study_materials(request):
    materials = StudyMaterial.objects.all()

    return render(
        request,
        'study_materials.html',
        {'materials': materials}
    )


@login_required
def assignments(request):
    assignments = Assignment.objects.all()

    return render(
        request,
        'assignments.html',
        {'assignments': assignments}
    )


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id
    )

    if request.method == 'POST':
        form = AssignmentSubmissionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            submission = form.save(commit=False)

            submission.assignment = assignment
            submission.student = request.user

            submission.save()

            return redirect('/assignments/')

    else:
        form = AssignmentSubmissionForm()

    return render(
        request,
        'submit_assignment.html',
        {
            'form': form,
            'assignment': assignment
        }
    )


@login_required
def quizzes(request):
    quizzes = Quiz.objects.all()

    return render(
        request,
        'quizzes.html',
        {'quizzes': quizzes}
    )


@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    questions = Question.objects.filter(
        quiz=quiz
    )

    if request.method == 'POST':
        score = 0

        for question in questions:
            selected_answer = request.POST.get(
                str(question.id)
            )

            if selected_answer == question.correct_answer:
                score += 1

        QuizResult.objects.create(
            student=request.user,
            quiz=quiz,
            score=score
        )

        return render(
            request,
            'quiz_result.html',
            {
                'score': score,
                'total': questions.count()
            }
        )

    return render(
        request,
        'take_quiz.html',
        {
            'quiz': quiz,
            'questions': questions
        }
    )


@login_required
def dashboard(request):
    enrolled_courses = Enrollment.objects.filter(
        student=request.user
    ).count()

    submitted_assignments = AssignmentSubmission.objects.filter(
        student=request.user
    ).count()

    quiz_attempts = QuizResult.objects.filter(
        student=request.user
    ).count()

    study_materials_count = StudyMaterial.objects.count()

    context = {
        'enrolled_courses': enrolled_courses,
        'submitted_assignments': submitted_assignments,
        'quiz_attempts': quiz_attempts,
        'study_materials': study_materials_count,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


def user_logout(request):
    logout(request)
    return redirect('/login/')

@login_required
def profile(request):

    enrolled_courses = Enrollment.objects.filter(
        student=request.user
    ).count()

    submitted_assignments = AssignmentSubmission.objects.filter(
        student=request.user
    ).count()

    quiz_attempts = QuizResult.objects.filter(
        student=request.user
    ).count()

    context = {
        'enrolled_courses': enrolled_courses,
        'submitted_assignments': submitted_assignments,
        'quiz_attempts': quiz_attempts,
    }

    return render(
        request,
        'profile.html',
        context
    )