/**
 * Test script to verify complete login -> jobs loading flow
 * Simulates what the frontend should do
 */

const BASE_URL = 'http://localhost:8000/api'

async function testCompleteFlow() {
  console.log('\n=====================================')
  console.log('TESTING COMPLETE LOGIN -> JOBS FLOW')
  console.log('=====================================\n')

  try {
    // STEP 1: Login
    console.log('STEP 1: Logging in...')
    const loginResponse = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'impulsombolivia@gmail.com',
        password: 'TestPassword123'
      })
    })

    const loginData = await loginResponse.json()
    console.log('✅ Login response received')
    console.log('   Status:', loginResponse.status)
    console.log('   Success:', loginData.success)
    console.log('   User:', loginData.user?.email)
    console.log('   Access Token:', loginData.tokens?.access ? '✓' : '✗')
    console.log('   Refresh Token:', loginData.tokens?.refresh ? '✓' : '✗')

    if (!loginData.success || !loginData.tokens?.access) {
      throw new Error('Login failed or no tokens returned')
    }

    const accessToken = loginData.tokens.access
    const userEmail = loginData.user.email

    // STEP 2: Load published jobs with fresh token
    console.log('\nSTEP 2: Loading published jobs...')
    const jobsResponse = await fetch(
      `${BASE_URL}/user/published?email=${encodeURIComponent(userEmail)}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      }
    )

    const jobsData = await jobsResponse.json()
    console.log('✅ Jobs response received')
    console.log('   Status:', jobsResponse.status)
    console.log('   Success:', jobsData.success)
    console.log('   Jobs count:', jobsData.jobs?.length || 0)

    if (jobsData.success && jobsData.jobs?.length > 0) {
      console.log('\n   Jobs found:')
      jobsData.jobs.forEach((job, idx) => {
        console.log(`   ${idx + 1}. ${job.title} (${job.status})`)
      })
    }

    console.log('\n=====================================')
    console.log('✅ COMPLETE FLOW TEST SUCCESSFUL')
    console.log('=====================================\n')

  } catch (error) {
    console.error('\n❌ ERROR:', error.message)
    console.log('=====================================\n')
  }
}

testCompleteFlow()
