"""
Vistas para visualización y descarga de reportes
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Report


def view_report(request, report_id):
    """
    Vista HTML del reporte para visualización e impresión
    """
    report = get_object_or_404(Report, id=report_id)

    context = {
        'report': report,
        'metrics': report.metrics,
    }

    return render(request, 'reports/report_view.html', context)


def download_report_html(request, report_id):
    """
    Descarga el reporte como archivo HTML autónomo
    """
    report = get_object_or_404(Report, id=report_id)

    html_string = render_to_string('reports/report_download.html', {
        'report': report,
        'metrics': report.metrics,
    })

    # Nombre del archivo
    filename = f"reporte_{report.get_report_type_display().lower()}_{report.period_start}_{report.period_end}.html"

    response = HttpResponse(html_string, content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
