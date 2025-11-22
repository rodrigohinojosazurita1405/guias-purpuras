from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import Job, Application


class JobAPITests(TestCase):
    """Tests para la app de trabajos"""

    def setUp(self):
        """Inicialización para cada test"""
        self.client = Client()
        self.job_data = {
            'title': 'Desarrollador Python',
            'companyName': 'Tech Company',
            'description': 'Buscamos un desarrollador Python senior',
            'jobCategory': 'Tecnología',
            'city': 'La Paz',
            'contractType': 'Tiempo Completo',
            'expiryDate': '2025-12-31',
            'requirements': 'Python, Django, SQL',
            'email': 'hr@techcompany.com',
            'whatsapp': '591-1234567890',
        }

    def test_publish_job_success(self):
        """Test para publicar una oferta de trabajo exitosamente"""
        response = self.client.post(
            reverse('jobs:publish_job'),
            data=json.dumps(self.job_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('id', data)
        self.assertEqual(Job.objects.count(), 1)

    def test_publish_job_missing_title(self):
        """Test para validar que el título es requerido"""
        job_data = self.job_data.copy()
        del job_data['title']

        response = self.client.post(
            reverse('jobs:publish_job'),
            data=json.dumps(job_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_publish_job_missing_description(self):
        """Test para validar que la descripción es requerida"""
        job_data = self.job_data.copy()
        del job_data['description']

        response = self.client.post(
            reverse('jobs:publish_job'),
            data=json.dumps(job_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_publish_job_missing_email(self):
        """Test para validar que el email es requerido"""
        job_data = self.job_data.copy()
        del job_data['email']

        response = self.client.post(
            reverse('jobs:publish_job'),
            data=json.dumps(job_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_list_jobs(self):
        """Test para listar trabajos activos"""
        # Crear un trabajo
        Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        response = self.client.get(reverse('jobs:list_jobs'))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['jobs']), 1)

    def test_get_job_detail(self):
        """Test para obtener detalles de un trabajo"""
        # Crear un trabajo
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        response = self.client.get(reverse('jobs:get_job', args=[job.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['job']['title'], 'Test Job')
        self.assertEqual(data['job']['id'], job.id)

        # Verificar que las vistas se incrementaron
        job.refresh_from_db()
        self.assertEqual(job.views, 1)

    def test_get_job_not_found(self):
        """Test para cuando un trabajo no existe"""
        response = self.client.get(reverse('jobs:get_job', args=['nonexistent']))

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_apply_to_job(self):
        """Test para aplicar a un trabajo"""
        # Crear un trabajo
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        apply_data = {
            'applicantName': 'Test Applicant',
            'applicantEmail': 'applicant@test.com',
            'screeningAnswers': {'0': 'Answer 1', '1': 'Answer 2'}
        }

        response = self.client.post(
            reverse('jobs:apply_to_job', args=[job.id]),
            data=json.dumps(apply_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

        # Verificar que las aplicaciones se incrementaron
        job.refresh_from_db()
        self.assertEqual(job.applications, 1)

    def test_apply_to_nonexistent_job(self):
        """Test para aplicar a un trabajo que no existe"""
        response = self.client.post(
            reverse('jobs:apply_to_job', args=['nonexistent'])
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_apply_with_complete_data(self):
        """Test para aplicar a un trabajo con datos completos"""
        # Crear un trabajo
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        apply_data = {
            'applicantName': 'Juan Pérez',
            'applicantEmail': 'juan@example.com',
            'applicantPhone': '1234567890',
            'applicantWhatsapp': '591-9876543210',
            'screeningAnswers': {
                '0': 'Respuesta 1',
                '1': 'Respuesta 2'
            }
        }

        response = self.client.post(
            reverse('jobs:apply_to_job', args=[job.id]),
            data=json.dumps(apply_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('applicationId', data)
        self.assertEqual(data['applicantAnswers'], apply_data['screeningAnswers'])

        # Verificar que la aplicación se guardó
        self.assertEqual(Application.objects.count(), 1)
        app = Application.objects.first()
        self.assertEqual(app.applicantName, 'Juan Pérez')
        self.assertEqual(app.applicantEmail, 'juan@example.com')

    def test_apply_missing_name(self):
        """Test para validar que el nombre es requerido"""
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        apply_data = {
            'applicantEmail': 'juan@example.com',
            'screeningAnswers': {'0': 'Respuesta 1'}
        }

        response = self.client.post(
            reverse('jobs:apply_to_job', args=[job.id]),
            data=json.dumps(apply_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('nombre', data['message'].lower())

    def test_apply_missing_email(self):
        """Test para validar que el email es requerido"""
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        apply_data = {
            'applicantName': 'Juan Pérez',
            'screeningAnswers': {'0': 'Respuesta 1'}
        }

        response = self.client.post(
            reverse('jobs:apply_to_job', args=[job.id]),
            data=json.dumps(apply_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('email', data['message'].lower())

    def test_duplicate_application(self):
        """Test para prevenir aplicaciones duplicadas del mismo candidato"""
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        apply_data = {
            'applicantName': 'Juan Pérez',
            'applicantEmail': 'juan@example.com',
            'screeningAnswers': {'0': 'Respuesta 1'}
        }

        # Primera aplicación
        response1 = self.client.post(
            reverse('jobs:apply_to_job', args=[job.id]),
            data=json.dumps(apply_data),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 201)

        # Segunda aplicación con el mismo email
        response2 = self.client.post(
            reverse('jobs:apply_to_job', args=[job.id]),
            data=json.dumps(apply_data),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 409)
        data = json.loads(response2.content)
        self.assertFalse(data['success'])
        self.assertIn('ya has aplicado', data['message'].lower())

    def test_list_applications(self):
        """Test para listar aplicaciones de un trabajo"""
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        # Crear dos aplicaciones
        Application.objects.create(
            job=job,
            applicantName='Juan Pérez',
            applicantEmail='juan@example.com',
            applicantPhone='1234567890',
            screeningAnswers={'0': 'Respuesta 1'}
        )

        Application.objects.create(
            job=job,
            applicantName='María García',
            applicantEmail='maria@example.com',
            applicantPhone='0987654321',
            screeningAnswers={'0': 'Respuesta 2'}
        )

        response = self.client.get(reverse('jobs:list_applications', args=[job.id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['applications']), 2)
        self.assertEqual(data['jobId'], job.id)
        self.assertEqual(data['jobTitle'], job.title)

    def test_list_applications_with_status_filter(self):
        """Test para listar aplicaciones filtrando por estado"""
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        # Crear aplicaciones con diferentes estados
        Application.objects.create(
            job=job,
            applicantName='Juan Pérez',
            applicantEmail='juan@example.com',
            status='received'
        )

        Application.objects.create(
            job=job,
            applicantName='María García',
            applicantEmail='maria@example.com',
            status='reviewing'
        )

        response = self.client.get(
            reverse('jobs:list_applications', args=[job.id]) + '?status=reviewing'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['applications'][0]['status'], 'reviewing')

    def test_update_application_status(self):
        """Test para actualizar el estado de una aplicación"""
        job = Job.objects.create(
            title='Test Job',
            companyName='Test Company',
            description='Test Description',
            jobCategory='Test',
            city='La Paz',
            contractType='Full-time',
            expiryDate='2025-12-31',
            requirements='Test',
            email='test@test.com',
            whatsapp='591-1234567890',
            status='active'
        )

        app = Application.objects.create(
            job=job,
            applicantName='Juan Pérez',
            applicantEmail='juan@example.com',
            status='received'
        )

        update_data = {
            'status': 'reviewing',
            'recruiterNotes': 'Excelente candidato'
        }

        response = self.client.patch(
            reverse('jobs:update_application_status', args=[job.id, app.id]),
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['application']['status'], 'reviewing')
        self.assertEqual(data['application']['recruiterNotes'], 'Excelente candidato')

        # Verificar que se actualizó en la BD
        app.refresh_from_db()
        self.assertEqual(app.status, 'reviewing')
        self.assertEqual(app.recruiterNotes, 'Excelente candidato')


class DashboardStatisticsTests(TestCase):
    """Tests para los endpoints de estadísticas del dashboard"""

    def setUp(self):
        """Inicialización para cada test"""
        self.client = Client()
        self.email = 'employer@company.com'
        self.applicant_email = 'candidate@example.com'

        # Crear trabajos
        self.job1 = Job.objects.create(
            title='Desarrollador Python',
            companyName='Tech Company',
            description='Buscamos desarrollador',
            jobCategory='Tecnología',
            city='La Paz',
            contractType='Tiempo Completo',
            expiryDate='2025-12-31',
            requirements='Python',
            email=self.email,
            whatsapp='591-1234567890',
            views=50,
            applications=3
        )

        self.job2 = Job.objects.create(
            title='Diseñador UX',
            companyName='Tech Company',
            description='Buscamos diseñador',
            jobCategory='Diseño',
            city='Cochabamba',
            contractType='Tiempo Completo',
            expiryDate='2025-12-31',
            requirements='Figma',
            email=self.email,
            whatsapp='591-1234567890',
            status='closed',
            views=30,
            applications=5
        )

        # Crear aplicaciones
        self.app1 = Application.objects.create(
            job=self.job1,
            applicantName='Juan Pérez',
            applicantEmail=self.applicant_email,
            applicantPhone='591-9876543210',
            status='received'
        )

        self.app2 = Application.objects.create(
            job=self.job1,
            applicantName='María García',
            applicantEmail='maria@example.com',
            applicantPhone='591-9876543211',
            status='shortlisted'
        )

    def test_get_user_statistics(self):
        """Test para obtener estadísticas del usuario"""
        response = self.client.get(
            f'/api/user/stats?email={self.email}'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        stats = data['statistics']

        self.assertEqual(stats['jobsPublished'], 2)
        self.assertEqual(stats['jobsActive'], 1)
        self.assertEqual(stats['applications'], 2)
        self.assertEqual(stats['applicationsNew'], 1)
        self.assertEqual(stats['totalViews'], 80)  # 50 + 30
        self.assertFalse(stats['profileComplete'])

    def test_get_user_statistics_no_email(self):
        """Test para obtener estadísticas sin email"""
        response = self.client.get('/api/user/stats')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        stats = data['statistics']

        self.assertEqual(stats['jobsPublished'], 0)
        self.assertEqual(stats['applications'], 0)

    def test_get_user_published_jobs(self):
        """Test para obtener trabajos publicados por el usuario"""
        response = self.client.get(
            f'/api/user/published?email={self.email}'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        jobs = data['jobs']

        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['title'], 'Diseñador UX')
        self.assertEqual(jobs[0]['views'], 30)
        self.assertEqual(jobs[0]['applications'], 5)

    def test_get_user_published_jobs_no_email(self):
        """Test para obtener trabajos sin email"""
        response = self.client.get('/api/user/published')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_get_user_applied_jobs(self):
        """Test para obtener trabajos a los que el usuario ha aplicado"""
        response = self.client.get(
            f'/api/user/applied?email={self.applicant_email}'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        applications = data['applications']

        self.assertEqual(len(applications), 1)
        self.assertEqual(applications[0]['jobTitle'], 'Desarrollador Python')
        self.assertEqual(applications[0]['status'], 'received')
        self.assertEqual(applications[0]['companyName'], 'Tech Company')

    def test_get_user_applied_jobs_no_email(self):
        """Test para obtener aplicaciones sin email"""
        response = self.client.get('/api/user/applied')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_get_user_activities(self):
        """Test para obtener actividades recientes del usuario"""
        response = self.client.get(
            f'/api/user/activities?email={self.email}'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        activities = data['activities']

        # Debe haber actividades de trabajos y aplicaciones
        self.assertGreater(len(activities), 0)
        self.assertLessEqual(len(activities), 5)

        # Verificar estructura de actividades
        for activity in activities:
            self.assertIn('type', activity)
            self.assertIn('title', activity)
            self.assertIn('date', activity)
            self.assertIn(activity['type'], ['job', 'application'])

    def test_get_user_activities_no_email(self):
        """Test para obtener actividades sin email"""
        response = self.client.get('/api/user/activities')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_get_user_activities_no_jobs(self):
        """Test para obtener actividades cuando no hay trabajos"""
        response = self.client.get(
            f'/api/user/activities?email=nonexistent@example.com'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        activities = data['activities']
        self.assertEqual(len(activities), 0)
