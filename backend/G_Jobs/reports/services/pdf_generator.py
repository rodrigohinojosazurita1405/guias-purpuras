"""
Servicio de generación de reportes (solo métricas, sin PDF)
"""
from datetime import date


def generate_report(report_type, start_date, end_date, user=None):
    """
    Genera un reporte (solo métricas, sin archivo PDF)

    Args:
        report_type (str): Tipo de reporte ('daily', 'weekly', 'monthly')
        start_date (date): Fecha de inicio del período
        end_date (date): Fecha de fin del período
        user (CustomUser, optional): Usuario que genera el reporte

    Returns:
        Report: Instancia del reporte generado con métricas
    """
    from G_Jobs.reports.models import Report
    from G_Jobs.reports.services.metrics import calculate_period_metrics

    # Crear el reporte en estado 'generating'
    report = Report.objects.create(
        report_type=report_type,
        period_start=start_date,
        period_end=end_date,
        status='generating',
        generated_by=user,
        metrics={}
    )

    try:
        # Calcular métricas del período
        metrics = calculate_period_metrics(start_date, end_date)

        # Guardar métricas y completar
        report.metrics = metrics
        report.status = 'completed'
        report.save()

        return report

    except Exception as e:
        # Si falla, marcar como fallido y guardar el error
        report.status = 'failed'
        report.error_message = str(e)
        report.save()
        raise


def regenerate_report(report_id):
    """
    Regenera las métricas de un reporte existente

    Args:
        report_id (int): ID del reporte a regenerar

    Returns:
        Report: Instancia del reporte actualizado
    """
    from G_Jobs.reports.models import Report
    from G_Jobs.reports.services.metrics import calculate_period_metrics

    report = Report.objects.get(id=report_id)

    try:
        # Actualizar estado
        report.status = 'generating'
        report.error_message = ''
        report.save()

        # Recalcular métricas
        metrics = calculate_period_metrics(report.period_start, report.period_end)
        report.metrics = metrics
        report.status = 'completed'
        report.save()

        return report

    except Exception as e:
        report.status = 'failed'
        report.error_message = str(e)
        report.save()
        raise


def generate_daily_report(target_date=None, user=None):
    """
    Genera un reporte diario

    Args:
        target_date (date, optional): Fecha del reporte. Por defecto es HOY
        user (CustomUser, optional): Usuario que genera el reporte

    Returns:
        Report: Reporte generado
    """
    from datetime import datetime

    if target_date is None:
        # Por defecto, generar reporte de HOY
        target_date = datetime.now().date()

    return generate_report('daily', target_date, target_date, user)


def generate_weekly_report(week_start=None, user=None):
    """
    Genera un reporte semanal (semana pasada completa: Lunes a Domingo)

    Args:
        week_start (date, optional): Lunes de la semana. Por defecto es SEMANA PASADA
        user (CustomUser, optional): Usuario que genera el reporte

    Returns:
        Report: Reporte generado
    """
    from datetime import datetime, timedelta

    if week_start is None:
        # Calcular lunes de la SEMANA PASADA
        today = datetime.now().date()
        days_since_monday = today.weekday()  # 0=Lunes, 6=Domingo
        current_week_monday = today - timedelta(days=days_since_monday)
        # Retroceder 7 días para obtener el lunes de la semana pasada
        week_start = current_week_monday - timedelta(days=7)

    # Calcular domingo (6 días después del lunes)
    week_end = week_start + timedelta(days=6)

    return generate_report('weekly', week_start, week_end, user)


def generate_last_7_days_report(user=None):
    """
    Genera un reporte de los últimos 7 días (hoy - 6 días hasta hoy)

    Args:
        user (CustomUser, optional): Usuario que genera el reporte

    Returns:
        Report: Reporte generado
    """
    from datetime import datetime, timedelta

    today = datetime.now().date()
    # Últimos 7 días: desde hace 6 días hasta hoy (inclusive)
    start_date = today - timedelta(days=6)
    end_date = today

    return generate_report('last_7_days', start_date, end_date, user)


def generate_monthly_report(year=None, month=None, user=None):
    """
    Genera un reporte mensual

    Args:
        year (int, optional): Año del reporte. Por defecto es ESTE MES
        month (int, optional): Mes del reporte (1-12). Por defecto es ESTE MES
        user (CustomUser, optional): Usuario que genera el reporte

    Returns:
        Report: Reporte generado
    """
    from datetime import datetime
    from calendar import monthrange

    if year is None or month is None:
        # Usar el mes ACTUAL
        today = datetime.now().date()
        year = today.year
        month = today.month

    # Primer día del mes
    month_start = date(year, month, 1)

    # Último día del mes
    last_day = monthrange(year, month)[1]
    month_end = date(year, month, last_day)

    return generate_report('monthly', month_start, month_end, user)
