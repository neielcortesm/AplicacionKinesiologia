from django.shortcuts import render, get_object_or_404
from .models import ExamenFinal, PreguntaExamenFinal

def pagina_5_subcategorias(request, examen_id):
    """
    AK-82: Mostrar las 3 subcategorías (síntoma, trabajo, actividades)
    asociadas al examen final.
    """

    examen = get_object_or_404(ExamenFinal, id=examen_id)

    subcategorias = [
        ('sintoma', 'Síntoma'),
        ('trabajo', 'Trabajo'),
        ('actividades', 'Actividades')
    ]

    context = {
        'examen': examen,
        'subcategorias': subcategorias
    }
    return render(request, 'examen/pagina_5.html', context)
def preguntas_por_subcategoria(request, examen_id, subcategoria_key):
    """
    AK-83: Mostrar preguntas filtradas por subcategoría.
    """
    examen = get_object_or_404(ExamenFinal, id=examen_id)

    preguntas = PreguntaExamenFinal.objects.filter(
        examen_final=examen,
        subcategoria=subcategoria_key
    )

    # Obtener el nombre legible
    labels = dict(PreguntaExamenFinal.CATEGORIAS)
    subcategoria_nombre = labels.get(subcategoria_key, subcategoria_key)

    context = {
        'examen': examen,
        'preguntas': preguntas,
        'subcategoria_key': subcategoria_key,
        'subcategoria_nombre': subcategoria_nombre,
    }

    return render(request, 'examen/pagina_5_subcategoria.html', context)
def guardar_preguntas_seleccionadas(request, examen_id, subcategoria_key):
    """
    AK-85: Guardar las preguntas seleccionadas al presionar Aceptar.
    """
    if request.method == 'POST':
        seleccionadas = request.POST.getlist('preguntas')

        if not seleccionadas:
            messages.error(request, "Debe seleccionar al menos una pregunta.")
            return redirect('preguntas_por_subcategoria', examen_id=examen_id, subcategoria_key=subcategoria_key)

        request.session[f"preguntas_{subcategoria_key}"] = seleccionadas

        messages.success(request, "Preguntas guardadas correctamente.")
        return redirect('pagina_5_subcategorias', examen_id=examen_id)
