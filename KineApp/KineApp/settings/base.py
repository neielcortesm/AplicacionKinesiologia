
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^*j72l#8&x)u2p4kh5j3lh15iw13pi()pj$s0zp*!=rs6#0hh^'

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #aplicaciones propias
    'applications.Categoria',
    'applications.Perfil',
    'applications.Paciente',
    'applications.Caso_Clinico',
    'applications.Examen',
    'applications.Etapa',
    'applications.Pregunta', 
     'Aestudiante',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'KineApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'KineApp.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    "site_title": "Administración App Kine UCN",
    "site_header": "Administración Kinesiología",
    "welcome_sign": "Bienvenida al Sistema de Casos Clínicos UCN",
    "site_brand": "Sistema Kinesiología",
    "site_logo": "img/logoucn_medicina.png",
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
    "icons": {
        "Caso_Clinico.CasoClinico": "fas fa-notes-medical",               # Casos clínicos
        "Categoria.Categoria": "fas fa-list",                      # Categorías
        "Etapa.Etapa": "fas fa-stream",                            # Etapas
        "Examen.ExamenFinal": "fas fa-file-alt",                   # Examen final
        "Examen.PreguntaExamenFinal": "fas fa-question-circle", # Preguntas examen final
        "Paciente.FichaPaciente": "fas fa-user-injured",           # Ficha paciente
        "Perfil.Administrador": "fas fa-user-shield",              # Administrador
        "Perfil.Docente": "fas fa-chalkboard-teacher",             # Docentes
        "Perfil.Estudiante": "fas fa-user-graduate",
        "Pregunta.Pregunta": "fas fa-question",                       # Preguntas
    },
     # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "Caso_Clinico"},
        {"app": "Categoria"},
        {"app": "Perfil"},
    ],
     # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],
    "default_icon_parents": "fas fa-folder",    # Icono por defecto de aplicaciones
    "default_icon_children": "fas fa-circle",
}
JAZZMIN_SETTINGS["icons"].update({
    "auth.Group": "fas fa-users-cog",    # Icono para Grupos
    "auth.User": "fas fa-user",          # Icono para Usuarios
})

LOGIN_URL = 'Aestudiante:login'
LOGIN_REDIRECT_URL = 'Inicio'          # ← tu inicio real
LOGOUT_REDIRECT_URL = 'Aestudiante:login'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'Aestudiante.auth_backends.EmailBackend',  # ← backend por correo
]

