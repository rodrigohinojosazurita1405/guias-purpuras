import json
from django.test import TestCase, Client
from .models import UserProfile, CompanyProfile


class UserProfileTestCase(TestCase):
    """Tests para UserProfile"""

    def setUp(self):
        self.client = Client()

    def test_create_user_profile_success(self):
        """Test crear perfil de usuario exitosamente"""
        response = self.client.post(
            '/api/profiles/user/create',
            data=json.dumps({
                'fullName': 'Juan Pérez',
                'email': 'juan@example.com',
                'phone': '1234567890',
                'location': 'La Paz',
                'bio': 'Ingeniero de software'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['fullName'], 'Juan Pérez')
        self.assertEqual(data['profile']['email'], 'juan@example.com')

    def test_create_user_profile_missing_name(self):
        """Test crear perfil sin nombre"""
        response = self.client.post(
            '/api/profiles/user/create',
            data=json.dumps({
                'email': 'juan@example.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_create_user_profile_missing_email(self):
        """Test crear perfil sin email"""
        response = self.client.post(
            '/api/profiles/user/create',
            data=json.dumps({
                'fullName': 'Juan Pérez'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_create_user_profile_duplicate_email(self):
        """Test prevenir duplicados de email"""
        # Crear primer perfil
        UserProfile.objects.create(
            fullName='Juan Pérez',
            email='juan@example.com'
        )

        # Intentar crear otro con el mismo email
        response = self.client.post(
            '/api/profiles/user/create',
            data=json.dumps({
                'fullName': 'Juan García',
                'email': 'juan@example.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
        data = response.json()
        self.assertFalse(data['success'])

    def test_get_user_profile_by_id(self):
        """Test obtener perfil de usuario por ID"""
        user = UserProfile.objects.create(
            fullName='Juan Pérez',
            email='juan@example.com',
            phone='1234567890',
            location='La Paz',
            bio='Ingeniero de software'
        )

        response = self.client.get(f'/api/profiles/user/{user.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['fullName'], 'Juan Pérez')

    def test_get_user_profile_by_email(self):
        """Test obtener perfil de usuario por email"""
        user = UserProfile.objects.create(
            fullName='Juan Pérez',
            email='juan@example.com'
        )

        response = self.client.get('/api/profiles/user/email/juan@example.com/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['id'], user.id)

    def test_get_user_profile_not_found(self):
        """Test obtener perfil inexistente"""
        response = self.client.get('/api/profiles/user/invalid123/')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertFalse(data['success'])

    def test_update_user_profile(self):
        """Test actualizar perfil de usuario"""
        user = UserProfile.objects.create(
            fullName='Juan Pérez',
            email='juan@example.com',
            phone='1111111111',
            location='La Paz'
        )

        response = self.client.patch(
            f'/api/profiles/user/{user.id}/edit',
            data=json.dumps({
                'phone': '2222222222',
                'location': 'Cochabamba'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Verificar cambios
        user.refresh_from_db()
        self.assertEqual(user.phone, '2222222222')
        self.assertEqual(user.location, 'Cochabamba')


class CompanyProfileTestCase(TestCase):
    """Tests para CompanyProfile"""

    def setUp(self):
        self.client = Client()
        # Crear usuario propietario
        self.user = UserProfile.objects.create(
            fullName='Admin User',
            email='admin@example.com'
        )

    def test_create_company_profile_success(self):
        """Test crear perfil de empresa exitosamente"""
        response = self.client.post(
            '/api/profiles/company/create',
            data=json.dumps({
                'userProfileId': self.user.id,
                'companyName': 'Tech Solutions',
                'description': 'Empresa de software',
                'email': 'contact@techsolutions.com',
                'phone': '1234567890',
                'website': 'https://techsolutions.com',
                'location': 'La Paz',
                'city': 'La Paz',
                'category': 'jobs'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['companyName'], 'Tech Solutions')

    def test_create_company_profile_missing_user(self):
        """Test crear empresa sin usuario propietario"""
        response = self.client.post(
            '/api/profiles/company/create',
            data=json.dumps({
                'companyName': 'Tech Solutions',
                'email': 'contact@techsolutions.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_create_company_profile_invalid_user(self):
        """Test crear empresa con usuario inválido"""
        response = self.client.post(
            '/api/profiles/company/create',
            data=json.dumps({
                'userProfileId': 'invalid',
                'companyName': 'Tech Solutions',
                'email': 'contact@techsolutions.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertFalse(data['success'])

    def test_get_company_profile(self):
        """Test obtener perfil de empresa"""
        company = CompanyProfile.objects.create(
            owner=self.user,
            companyName='Tech Solutions',
            description='Empresa de software',
            email='contact@techsolutions.com',
            phone='1234567890',
            website='https://techsolutions.com',
            location='La Paz',
            city='La Paz',
            category='jobs'
        )

        response = self.client.get(f'/api/profiles/company/{company.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['companyName'], 'Tech Solutions')

    def test_get_company_profile_not_found(self):
        """Test obtener empresa inexistente"""
        response = self.client.get('/api/profiles/company/invalid/')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertFalse(data['success'])

    def test_update_company_profile(self):
        """Test actualizar perfil de empresa"""
        company = CompanyProfile.objects.create(
            owner=self.user,
            companyName='Tech Solutions',
            email='contact@techsolutions.com',
            location='La Paz'
        )

        response = self.client.patch(
            f'/api/profiles/company/{company.id}/edit',
            data=json.dumps({
                'companyName': 'Tech Pro Solutions',
                'location': 'Cochabamba'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Verificar cambios
        company.refresh_from_db()
        self.assertEqual(company.companyName, 'Tech Pro Solutions')
        self.assertEqual(company.location, 'Cochabamba')

    def test_list_user_companies(self):
        """Test listar empresas del usuario"""
        # Crear múltiples empresas
        CompanyProfile.objects.create(
            owner=self.user,
            companyName='Tech Solutions',
            email='tech@example.com',
            category='jobs'
        )
        CompanyProfile.objects.create(
            owner=self.user,
            companyName='Food Corp',
            email='food@example.com',
            category='restaurant'
        )

        response = self.client.get(f'/api/profiles/user/{self.user.id}/companies')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['companies']), 2)

    def test_list_user_companies_empty(self):
        """Test listar empresas cuando no hay"""
        response = self.client.get(f'/api/profiles/user/{self.user.id}/companies')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['companies']), 0)

    def test_list_user_companies_invalid_user(self):
        """Test listar empresas con usuario inválido"""
        response = self.client.get('/api/profiles/user/invalid/companies')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertFalse(data['success'])
