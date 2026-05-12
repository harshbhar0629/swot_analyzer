from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('category/', views.category_view, name='category'),
    path('idea/', views.idea_view, name='idea'),
    path('result/', views.result_view, name='result'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('about/', views.about, name='about'),
    path('concept/', views.concept, name='concept'),
    path('working/', views.working, name='working'),
]
