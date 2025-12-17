import requests
import json

BASE_URL = 'http://localhost:8000'

# Step 1: Login as Maria Varquera
print("=" * 60)
print("STEP 1: Logging in as Maria Varquera (mauge@gmail.com)")
print("=" * 60)

login_response = requests.post(
    f'{BASE_URL}/api/auth/login',
    json={
        'email': 'mauge@gmail.com',
        'password': 'iluminaty1405@'
    }
)

print(f"Login Status: {login_response.status_code}")

if login_response.status_code == 200:
    login_data = login_response.json()
    print(f"Login Success: {login_data.get('success')}")
    print(f"User: {login_data.get('user', {}).get('email')}")

    # Extract access token
    access_token = login_data['tokens']['access']
    print(f"Access Token: {access_token[:50]}...")

    # Step 2: Submit application to job "cd2dc7ad" (Arquitecto Senior)
    print("\n" + "=" * 60)
    print("STEP 2: Submitting application to job 'cd2dc7ad'")
    print("=" * 60)

    job_id = 'cd2dc7ad'

    application_data = {
        'cv_id': None,  # No CV for this test
        'cover_letter': 'Soy María Varquera y estoy interesada en esta posición de Arquitecto Senior. Tengo experiencia en diseño arquitectónico y manejo de proyectos.',
        'screening_answers': {}
    }

    application_response = requests.post(
        f'{BASE_URL}/api/apply/{job_id}/',
        json=application_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )

    print(f"Application Status: {application_response.status_code}")
    print(f"Response: {json.dumps(application_response.json(), indent=2, ensure_ascii=False)}")

    if application_response.status_code == 201:
        app_data = application_response.json()
        print("\n✅ APPLICATION SUBMITTED SUCCESSFULLY!")
        print(f"Application ID: {app_data.get('application', {}).get('id')}")
        print(f"Job: {app_data.get('application', {}).get('job_title')}")
        print(f"Status: {app_data.get('application', {}).get('status')}")
        print("\n🔍 Check Django Admin at:")
        print(f"   http://localhost:8000/admin/applicants/jobapplication/")
    else:
        print("\n❌ APPLICATION FAILED")

else:
    print(f"Login Failed: {login_response.text}")
