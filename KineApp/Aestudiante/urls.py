from django.urls import path
from .views import LoginView, RegisterView, logout_view

app_name = "Aestudiante"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registro/", RegisterView.as_view(), name="registro"),
    path("logout/", logout_view, name="logout"),
]
