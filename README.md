# AplicacionKinesiologia
Proyecto "KineApp" 
    Sistema de Gestión de Casos Clínicos

*Descripción del Proyecto
KineApp es una aplicación web desarrollada con Django que permite gestionar los casos clínicos, pacientes, docentes, estudiantes y las etapas del tratamiento kinesiológico en un entorno académico.
Su objetivo es facilitar el registro, seguimiento y evaluación de los procesos clínicos de forma digital, moderna y segura, reemplazando los registros manuales.

*Integrantes del Equipo
Nombre	        Rol	                   Módulo
Neiel Cortes	Product Owner   App etapas, personalizacion Jazzmin, documentar evidencias, readme
Daniela Cofre	Scrum Master	App casos_clinicos, configuracion claves foraneas
Luz Azocar	    Desarrollador	App Pregunta, respuesta
Joaquin Serey	Desarrollador	App Pregunta_Estudiante
Javiera Pizarro	Desarrollador	App  Examen Final
Ruben Cortes	Desarrollador	App Preguntas_ExF, Respuestas_ExF
Jocelyn Leon	Desarrollador   App Perfil
Belen Andrades	Desarrollador	App Ficha_Paciente, Categoria

*Instalación y Ejecución
1. Clonar el repositorio:
    git clone https://github.com/tuusuario/proyecto-kinesiologia.git
    cd proyecto-kinesiologia

2. Crear y activar entorno virtual:
    python -m venv entornoKinesiologia
    entornoKinesiologia\Scripts\activate

3. Instalar dependencias:
    pip install -r requirements.txt

4. Aplicar migraciones:
    python manage.py makemigrations
    python manage.py migrate

5. Crear superusuario:
    python manage.py createsuperuser

6. Ejecutar el servidor:
    python manage.py runserver

7. Acceder al panel:
    Sitio: http://localhost:8000/
    Admin: http://localhost:8000/admin/

*Configuración de Base de Datos (PostgreSQL):
En el archivo settings.py, actualizar la sección DATABASES con tus datos reales:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kineapp_db',
        'USER': 'postgres',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}