from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('login-page/', views.loginView, name='login-page'),
    path('logout-page/', views.logoutView, name='logout-page'),
    path('register-page/', views.registerView, name='register-page'),
]
