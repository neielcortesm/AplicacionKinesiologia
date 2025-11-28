from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, RegisterForm

class LoginView(View):
    template_name = "Aestudiante/login.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("Inicio")
        return render(request, self.template_name, {"form": LoginForm()})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower().strip()
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("Inicio")
            messages.error(request, "Correo o contraseña incorrectos.")
        return render(request, self.template_name, {"form": form})

class RegisterView(View):
    template_name = "Aestudiante/registro.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("Inicio")
        return render(request, self.template_name, {"form": RegisterForm()})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw = form.cleaned_data["password1"]
            user = authenticate(request, email=user.email, password=raw)
            if user:
                login(request, user)
                return redirect("Inicio")
        return render(request, self.template_name, {"form": form})

def logout_view(request):
    logout(request)
    return redirect("Aestudiante:login")
