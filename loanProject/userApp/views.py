from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, LoginForm

def user_registration(request):
      if request.method == 'POST':
          form = UserRegistrationForm(request.POST)
          if form.is_valid():
              user = form.save()
              login(request, user)
              return redirect('dashboard')
      else:
          form = UserRegistrationForm()
      return render(request, 'userApp/registration.html', {'form': form})

def user_login(request):
      if request.method == 'POST':
          form = LoginForm(request, data=request.POST)
          if form.is_valid():
              email = form.cleaned_data.get('username')
              password = form.cleaned_data.get('password')
              user = authenticate(request, email=email, password=password)
              if user is not None:
                  login(request, user)
                  return redirect('dashboard')
      else:
          form = LoginForm()
      return render(request, 'userApp/login.html', {'form': form})

def dashboard(request):
      return render(request, 'userApp/dashboard.html')


#def pour supprimer un user en tant que conseiller