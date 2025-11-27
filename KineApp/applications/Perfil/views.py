from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Docente

# --------- Decorador: protege vistas solo para docentes ----------
def docente_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('docente_id'):
            messages.warning(request, "Debes iniciar sesión como docente.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped

# --------- LOGIN DOCENTE (correo + contraseña) ----------
def login_view(request):
    if request.method == 'POST':
        correo = (request.POST.get('correo') or '').strip().lower()
        contrasena = (request.POST.get('contrasena') or '').strip()

        # Busca docente activo por correo (case-insensitive) y contraseña
        docente = Docente.objects.filter(
            correo__iexact=correo, contrasena=contrasena, estado=True
        ).first()

        if docente:
    # guarda lo necesario para mostrar la tarjeta en HOME
            request.session['docente_id'] = docente.id
            request.session['docente_nombre'] = f"{docente.nombre} {docente.apellido}"
            request.session['docente_correo'] = docente.correo
            request.session['docente_estado'] = "Activo" if docente.estado else "Inactivo"

            request.session.set_expiry(60 * 60)  # 60 min

    # 🔁 envía al HOME
    # Si tu URL del home se llama 'home', usa:
            return redirect('home')
        messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, 'login.html')

def logout_view(request):
    for k in ['docente_id', 'docente_nombre', 'docente_correo', 'docente_estado', 'login_fails']:
        request.session.pop(k, None)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')  
# --------- PANEL DOCENTE (protegido) ----------
@docente_login_required
def panel_docente(request):
    docente_id = request.session.get('docente_id')
    try:
        docente = Docente.objects.get(id=docente_id, estado=True)
    except Docente.DoesNotExist:
        # si el docente ya no existe o está inactivo, limpia la sesión
        request.session.pop('docente_id', None)
        messages.warning(request, "Tu sesión ya no es válida. Inicia nuevamente.")
        return redirect('login')

    return render(request, 'panel_docente.html', {'docente': docente})