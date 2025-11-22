// Simular lo que pasa con localStorage
console.log("=== ANTES DE LOGOUT ===")
localStorage.setItem('access_token', 'test_token_123')
localStorage.setItem('refresh_token', 'test_refresh_123')
localStorage.setItem('auth_user', JSON.stringify({name: 'Test User', email: 'test@test.com'}))

console.log('access_token:', localStorage.getItem('access_token'))
console.log('auth_user:', localStorage.getItem('auth_user'))

console.log("\n=== DESPUÉS DE LOGOUT ===")
localStorage.clear()
console.log('access_token:', localStorage.getItem('access_token'))
console.log('auth_user:', localStorage.getItem('auth_user'))
console.log('localStorage.length:', localStorage.length)

console.log("\n=== DESPUÉS DE sessionStorage.clear() ===")
sessionStorage.clear()
console.log('sessionStorage.length:', sessionStorage.length)
