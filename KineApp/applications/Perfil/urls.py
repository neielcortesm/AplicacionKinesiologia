from django.urls import path
from .views import login_view, panel_docente, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('docente/panel/', panel_docente, name='panel_docente'),
    path('logout/', logout_view, name='logout'),
]
