from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FeedbackForm, RegisterForm
from .models import SWOTAnalysis
from .openai_client import SWOTGenerationError, generate_swot


CATEGORIES = [
    'Education', 'Hospitality', 'Health', 'Finance', 'Music',
    'Food', 'Nationality', 'Travel', 'Household'
]


def home(request):
    return render(request, 'mainapp/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('category')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Registration successful.')
        return redirect('category')

    return render(request, 'mainapp/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('category')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                messages.success(request, 'Successfully logged in.')
                return redirect('category')

        messages.error(request, 'Login failed.')

    return render(request, 'mainapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def category_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        request.session['category'] = category
        return redirect('idea')

    return render(request, 'mainapp/category.html', {'categories': CATEGORIES})


@login_required
def idea_view(request):
    category = request.session.get('category')

    if not category:
        return redirect('category')

    if request.method == 'POST':
        idea = request.POST.get('idea', '').strip()

        if not idea:
            messages.error(request, 'Please enter your idea.')
            return render(request, 'mainapp/idea.html', {'category': category})

        try:
            swot = generate_swot(idea, category)
        except SWOTGenerationError as exc:
            messages.error(request, str(exc))
            return render(request, 'mainapp/idea.html', {'category': category, 'idea': idea})

        analysis = SWOTAnalysis.objects.create(
            user=request.user,
            category=category,
            idea=idea,
            strengths=swot['strengths'],
            weaknesses=swot['weaknesses'],
            opportunities=swot['opportunities'],
            threats=swot['threats'],
        )

        request.session['analysis_id'] = analysis.pk
        return redirect('result')

    return render(request, 'mainapp/idea.html', {'category': category})


@login_required
def result_view(request):
    analysis_id = request.session.get('analysis_id')
    analysis = get_object_or_404(SWOTAnalysis, id=analysis_id, user=request.user)
    return render(request, 'mainapp/result.html', {'analysis': analysis})


@login_required
def feedback_view(request):
    form = FeedbackForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.save()
        messages.success(request, 'Feedback saved.')
        return redirect('home')

    return render(request, 'mainapp/feedback.html', {'form': form})


def about(request):
    return render(request, 'mainapp/about.html')


def concept(request):
    return render(request, 'mainapp/concept.html')


def working(request):
    return render(request, 'mainapp/working.html')
