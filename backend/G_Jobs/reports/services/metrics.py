"""
Servicio de cálculo de métricas para reportes
"""
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone


def calculate_period_metrics(start_date, end_date):
    """
    Calcula todas las métricas para un período específico

    Args:
        start_date (date): Fecha de inicio del período
        end_date (date): Fecha de fin del período

    Returns:
        dict: Diccionario con todas las métricas calculadas
    """
    from auth_api.models import CustomUser
    from G_Jobs.jobs.models import Job
    from G_Jobs.payments.models import PlanOrder
    from G_Jobs.applicants.models import JobApplication

    # Calcular duración del período para comparaciones
    period_days = (end_date - start_date).days + 1
    previous_start = start_date - timedelta(days=period_days)
    previous_end = start_date - timedelta(days=1)

    # === USUARIOS ===
    users_metrics = _calculate_users_metrics(start_date, end_date, previous_start, previous_end)

    # === TRABAJOS ===
    jobs_metrics = _calculate_jobs_metrics(start_date, end_date, previous_start, previous_end)

    # === PLANES ===
    plans_metrics = _calculate_plans_metrics(start_date, end_date, previous_start, previous_end)

    # === INGRESOS ===
    revenue_metrics = _calculate_revenue_metrics(start_date, end_date, previous_start, previous_end)

    # === APLICACIONES ===
    applications_metrics = _calculate_applications_metrics(start_date, end_date, previous_start, previous_end)

    # === COMPARACIONES ===
    comparison = _calculate_comparisons(
        users_metrics, jobs_metrics, plans_metrics, revenue_metrics, applications_metrics
    )

    # === INSIGHTS AUTOMÁTICOS ===
    insights = _generate_insights(
        users_metrics, jobs_metrics, plans_metrics, revenue_metrics,
        applications_metrics, comparison
    )

    return {
        'period': {
            'type': _get_period_type(start_date, end_date),
            'start': start_date.isoformat(),
            'end': end_date.isoformat(),
            'label': _get_period_label(start_date, end_date),
            'days': period_days,
        },
        'users': users_metrics,
        'jobs': jobs_metrics,
        'plans': plans_metrics,
        'revenue': revenue_metrics,
        'applications': applications_metrics,
        'comparison': comparison,
        'insights': insights,
        'generated_at': timezone.now().isoformat(),
    }


def _calculate_users_metrics(start_date, end_date, previous_start, previous_end):
    """Calcula métricas de usuarios"""
    from auth_api.models import CustomUser

    # Usuarios del período actual
    new_users = CustomUser.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).count()

    new_companies = CustomUser.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
        role='company'
    ).count()

    new_applicants = CustomUser.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
        role='applicant'
    ).count()

    # Usuarios del período anterior
    previous_new_users = CustomUser.objects.filter(
        created_at__date__gte=previous_start,
        created_at__date__lte=previous_end
    ).count()

    # Totales acumulados
    total_users = CustomUser.objects.count()
    total_companies = CustomUser.objects.filter(role='company').count()
    total_applicants = CustomUser.objects.filter(role='applicant').count()
    active_users = CustomUser.objects.filter(is_active=True).count()

    return {
        'new_total': new_users,
        'new_companies': new_companies,
        'new_applicants': new_applicants,
        'total_accumulated': total_users,
        'total_companies': total_companies,
        'total_applicants': total_applicants,
        'active_users': active_users,
        'previous_new_total': previous_new_users,
    }


def _calculate_jobs_metrics(start_date, end_date, previous_start, previous_end):
    """Calcula métricas de trabajos"""
    from G_Jobs.jobs.models import Job

    # Trabajos del período actual
    new_jobs = Job.objects.filter(
        createdAt__date__gte=start_date,
        createdAt__date__lte=end_date,
        isDeleted=False
    ).count()

    jobs_closed_in_period = Job.objects.filter(
        updatedAt__date__gte=start_date,
        updatedAt__date__lte=end_date,
        status='closed',
        isDeleted=False
    ).count()

    # Trabajos del período anterior
    previous_new_jobs = Job.objects.filter(
        createdAt__date__gte=previous_start,
        createdAt__date__lte=previous_end,
        isDeleted=False
    ).count()

    # Snapshots actuales
    active_jobs = Job.objects.filter(
        status='active',
        paymentVerified=True,
        isDeleted=False
    ).count()

    closed_jobs = Job.objects.filter(
        status='closed',
        isDeleted=False
    ).count()

    total_views = Job.objects.filter(
        isDeleted=False
    ).aggregate(Sum('views'))['views__sum'] or 0

    # Top trabajos del período
    top_jobs = list(Job.objects.filter(
        createdAt__date__gte=start_date,
        createdAt__date__lte=end_date,
        isDeleted=False
    ).order_by('-views')[:5].values('id', 'title', 'views'))

    return {
        'new': new_jobs,
        'closed_in_period': jobs_closed_in_period,
        'active': active_jobs,
        'closed': closed_jobs,
        'total_views': total_views,
        'previous_new': previous_new_jobs,
        'top_jobs': top_jobs,
    }


def _calculate_plans_metrics(start_date, end_date, previous_start, previous_end):
    """Calcula métricas de planes vendidos"""
    from G_Jobs.payments.models import PlanOrder

    # Órdenes del período actual
    orders = PlanOrder.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
        status='completed'
    )

    total_sold = orders.count()
    estandar_count = orders.filter(selected_plan='estandar').count()
    purpura_count = orders.filter(selected_plan='purpura').count()
    impulso_count = orders.filter(selected_plan='impulso').count()

    # Órdenes del período anterior
    previous_orders = PlanOrder.objects.filter(
        created_at__date__gte=previous_start,
        created_at__date__lte=previous_end,
        status='completed'
    )
    previous_total_sold = previous_orders.count()

    # Determinar plan más vendido
    plans_by_count = [
        ('estandar', estandar_count),
        ('purpura', purpura_count),
        ('impulso', impulso_count),
    ]
    most_sold = max(plans_by_count, key=lambda x: x[1])[0] if total_sold > 0 else None

    # Distribución porcentual
    distribution = {}
    if total_sold > 0:
        distribution = {
            'estandar': round((estandar_count / total_sold) * 100, 1),
            'purpura': round((purpura_count / total_sold) * 100, 1),
            'impulso': round((impulso_count / total_sold) * 100, 1),
        }

    # Top empresas por planes comprados
    top_companies = list(orders.values('user__id', 'user__email')
                        .annotate(plans_bought=Count('id'))
                        .order_by('-plans_bought')[:5])

    return {
        'total_sold': total_sold,
        'by_type': {
            'estandar': estandar_count,
            'purpura': purpura_count,
            'impulso': impulso_count,
        },
        'most_sold': most_sold,
        'distribution': distribution,
        'previous_total_sold': previous_total_sold,
        'top_companies': top_companies,
    }


def _calculate_revenue_metrics(start_date, end_date, previous_start, previous_end):
    """Calcula métricas de ingresos"""
    from G_Jobs.payments.models import PlanOrder

    # Órdenes del período actual
    orders = PlanOrder.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
        status='completed'
    )

    total_revenue = orders.aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')
    estandar_revenue = orders.filter(selected_plan='estandar').aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')
    purpura_revenue = orders.filter(selected_plan='purpura').aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')
    impulso_revenue = orders.filter(selected_plan='impulso').aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')

    # Ticket promedio
    average_ticket = total_revenue / orders.count() if orders.count() > 0 else Decimal('0')

    # Órdenes del período anterior
    previous_orders = PlanOrder.objects.filter(
        created_at__date__gte=previous_start,
        created_at__date__lte=previous_end,
        status='completed'
    )
    previous_total_revenue = previous_orders.aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')

    # Top empresas por ingresos
    top_companies_revenue = []
    for company in orders.values('user__id', 'user__email').annotate(total_spent=Sum('plan_price')).order_by('-total_spent')[:5]:
        company['total_spent'] = float(company['total_spent'] or 0)
        top_companies_revenue.append(company)

    return {
        'total': float(total_revenue),
        'by_plan': {
            'estandar': float(estandar_revenue),
            'purpura': float(purpura_revenue),
            'impulso': float(impulso_revenue),
        },
        'average_ticket': float(average_ticket),
        'previous_total': float(previous_total_revenue),
        'top_companies': top_companies_revenue,
    }


def _calculate_applications_metrics(start_date, end_date, previous_start, previous_end):
    """Calcula métricas de aplicaciones"""
    from G_Jobs.applicants.models import JobApplication
    from G_Jobs.jobs.models import Job

    # Aplicaciones del período actual
    applications = JobApplication.objects.filter(
        applied_at__date__gte=start_date,
        applied_at__date__lte=end_date
    )

    total_applications = applications.count()

    # Aplicaciones del período anterior
    previous_applications = JobApplication.objects.filter(
        applied_at__date__gte=previous_start,
        applied_at__date__lte=previous_end
    ).count()

    # Trabajos con aplicaciones en el período
    jobs_with_applications = applications.values('job_id').distinct().count()

    # Promedio de aplicaciones por trabajo
    avg_applications_per_job = 0
    if jobs_with_applications > 0:
        avg_applications_per_job = round(total_applications / jobs_with_applications, 1)

    # Top trabajos por aplicaciones en el período
    top_jobs = list(applications.values('job__id', 'job__title')
                   .annotate(applications_count=Count('id'))
                   .order_by('-applications_count')[:5])

    return {
        'total': total_applications,
        'previous_total': previous_applications,
        'jobs_with_applications': jobs_with_applications,
        'average_per_job': avg_applications_per_job,
        'top_jobs': top_jobs,
    }


def _calculate_comparisons(users, jobs, plans, revenue, applications):
    """Calcula comparaciones con período anterior"""

    def calculate_change(current, previous):
        """Calcula el cambio porcentual"""
        if previous == 0:
            return {'amount': current, 'percent': 100.0 if current > 0 else 0, 'direction': 'up' if current > 0 else 'neutral'}

        change_amount = current - previous
        change_percent = round((change_amount / previous) * 100, 1)
        direction = 'up' if change_amount > 0 else ('down' if change_amount < 0 else 'neutral')

        return {
            'amount': change_amount,
            'percent': abs(change_percent),
            'direction': direction,
        }

    return {
        'users': calculate_change(users['new_total'], users['previous_new_total']),
        'jobs': calculate_change(jobs['new'], jobs['previous_new']),
        'plans': calculate_change(plans['total_sold'], plans['previous_total_sold']),
        'revenue': calculate_change(revenue['total'], revenue['previous_total']),
        'applications': calculate_change(applications['total'], applications['previous_total']),
    }


def _generate_insights(users, jobs, plans, revenue, applications, comparison):
    """Genera insights automáticos basados en las métricas"""
    insights = []

    # Insight sobre ingresos
    if comparison['revenue']['direction'] == 'up':
        insights.append(f"Los ingresos aumentaron {comparison['revenue']['percent']}% respecto al período anterior")
    elif comparison['revenue']['direction'] == 'down':
        insights.append(f"ALERTA: Los ingresos disminuyeron {comparison['revenue']['percent']}% respecto al período anterior")

    # Insight sobre plan más vendido
    if plans['most_sold']:
        plan_names = {'estandar': 'Estándar', 'purpura': 'Púrpura', 'impulso': 'Impulso'}
        insights.append(f"El plan {plan_names[plans['most_sold']]} fue el más vendido con {plans['distribution'][plans['most_sold']]}% de participación")

    # Insight sobre nuevos usuarios
    if comparison['users']['direction'] == 'up':
        insights.append(f"Se registraron {users['new_total']} nuevos usuarios ({comparison['users']['percent']}% más que el período anterior)")

    # Insight sobre trabajos
    if jobs['new'] > 0:
        insights.append(f"Se publicaron {jobs['new']} nuevos trabajos en el período")

    # Insight sobre aplicaciones
    if applications['average_per_job'] > 0:
        insights.append(f"Promedio de {applications['average_per_job']} aplicaciones por trabajo publicado")

    # Alertas
    if revenue['total'] == 0:
        insights.append("ALERTA: No se registraron ingresos en este período")

    if plans['total_sold'] == 0:
        insights.append("ALERTA: No se vendieron planes en este período")

    return insights


def _get_period_type(start_date, end_date):
    """Determina el tipo de período basado en las fechas"""
    days = (end_date - start_date).days + 1

    if days == 1:
        return 'daily'
    elif 6 <= days <= 8:
        return 'weekly'
    elif 28 <= days <= 31:
        return 'monthly'
    else:
        return 'custom'


def _get_period_label(start_date, end_date):
    """Genera una etiqueta legible para el período"""
    from datetime import date

    days = (end_date - start_date).days + 1

    if days == 1:
        months_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        return f"{start_date.day} de {months_es[start_date.month]} {start_date.year}"
    elif days == 7:
        # Exactamente 7 días - verificar si es semana calendario o últimos 7 días
        # Si empieza en lunes, es semana calendario
        if start_date.weekday() == 0:  # 0 = Lunes
            return f"{start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m/%Y')}"
        else:
            # Últimos 7 días
            return f"Ultimos 7 dias ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m/%Y')})"
    elif 6 <= days <= 8:
        return f"Semana del {start_date.strftime('%d/%m')} al {end_date.strftime('%d/%m/%Y')}"
    elif 28 <= days <= 31:
        months_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        return f"{months_es[start_date.month]} {start_date.year}"
    else:
        return f"Del {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}"
