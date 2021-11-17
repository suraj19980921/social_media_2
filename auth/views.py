from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from auth import forms
from main import models
from django.views.generic import View
from django.shortcuts import redirect

# Create your views here.

class Login(LoginView):
    template_name = 'auth/login.html'
    form_class = forms.LoginForm
    success_url = '/'
    
    def get_success_url(self):
        models.Profile.objects.filter(user = self.request.user).update(online = True)
        return super().get_success_url()

class Logout(View):
    
    def get(self,request):
        models.Profile.objects.filter(user = self.request.user).update(online = False)
        logout(self.request)
        return redirect('/auth/login')



class Singup(CreateView):
    template_name = 'auth/signup.html'
    form_class = forms.SingupForm
    success_url = '/auth/login/'