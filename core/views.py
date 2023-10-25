from django.shortcuts import render
from .models import Customer
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='login-page')
def home(request):
    context = {
        
    }
    return render(request, 'gym/home.html', context = context)

