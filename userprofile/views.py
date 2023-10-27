from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .serilizers import UserSerializer
from .models import User
# import jwt, datetime
import requests
import json

from userprofile.models import User  # Import your custom User model
from userprofile.forms import CustomUserCreationForm  # Import your custom registration form
# Create your views here.
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Only users who are both authenticated and staff (admin) can access the view.


class RegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('homePage')

    def form_valid(self, form):
        # Auto-login after successful registration
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    @method_decorator(user_passes_test(is_admin, login_url='login-page'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

    @method_decorator(user_passes_test(is_admin, login_url='homePage'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)



class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)  # Log in the user
            messages.success(request, 'Login successful.')
            return redirect('homePage')  # Replace 'homePage' with your desired redirect URL
        else:
            messages.error(request, 'Login failed. Please check your email and password.')
    else:
        # If the user is already authenticated, log them out before showing the login page
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'auth/login.html')

    return render(request, 'auth/login.html')
    
def logoutView(request):
    # logoutUrl = 'http://127.0.0.1:8000/cred/logout/'
    # response = requests.post(logoutUrl)
    logout(request)
    return redirect('login-page')


def registerView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('homePage')  # Replace 'homePage' with your desired redirect URL
        else:
            print(form.errors)
            print("form validation failed")
            messages.error(request, "There was an error registering the user! Try again ")
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

# def reigsterView(request):
    
#     if request.method == 'POST':
#         if request.user == 'Anonymous':
#             print('Yes')
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         data = {
#             "email": email,
#             "password": password,
#             "username": username
#         }
#         print(data)
#         login_url = 'http://127.0.0.1:8000/cred/register/'
#         response = requests.post(login_url, data=data)
#         res_content = response.json()
#         jwt_cookie = request.ge
#         # print(res_content)
#         if response.status_code == 200:
#             user = User.objects.get(email= email)
#             login(request, user)
#             return redirect('homePage')
#         else:
#             messages.error(request, res_content['detail'])
#             return render(request, 'auth/login.html')
#     else:
#         return render(request, 'auth/register.html')


