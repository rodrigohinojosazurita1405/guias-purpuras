/**
 * Composable para calcular la completitud del perfil de usuario
 * Bloquea postulaciones si el perfil no está completo al menos al 80%
 */

/**
 * Calcula el porcentaje de completitud del perfil
 * @param {Object} profile - Perfil del usuario
 * @returns {Object} - { percentage, missingFields, canApply }
 */
export function calculateProfileCompletion(profile) {
  if (!profile) {
    return {
      percentage: 0,
      missingFields: ['Perfil no encontrado'],
      canApply: false,
      requiredFields: []
    }
  }

  // Campos obligatorios para poder postular (80% de completitud)
  const requiredFields = [
    {
      key: 'profilePhoto',
      label: 'Foto de perfil',
      value: profile.profilePhoto,
      check: (val) => val && val.trim() !== ''
    },
    {
      key: 'fullName',
      label: 'Nombre completo',
      value: profile.fullName,
      check: (val) => val && val.trim() !== ''
    },
    {
      key: 'ci',
      label: 'Cédula de Identidad (C.I.)',
      value: profile.ci,
      check: (val) => val && val.trim() !== ''
    },
    {
      key: 'nationality',
      label: 'Nacionalidad',
      value: profile.nationality,
      check: (val) => val && val.trim() !== ''
    },
    {
      key: 'phone',
      label: 'WhatsApp',
      value: profile.phone,
      check: (val) => val && val.trim() !== ''
    }
  ]

  // Calcular campos completados
  const completedFields = requiredFields.filter(field =>
    field.check(field.value)
  )

  // Calcular campos faltantes
  const missingFields = requiredFields
    .filter(field => !field.check(field.value))
    .map(field => field.label)

  // Calcular porcentaje
  const percentage = Math.round((completedFields.length / requiredFields.length) * 100)

  // Puede postular si tiene al menos 80% completado (4 de 5 campos)
  const canApply = percentage >= 80

  return {
    percentage,
    missingFields,
    canApply,
    requiredFields: requiredFields.map(f => ({
      key: f.key,
      label: f.label,
      completed: f.check(f.value)
    }))
  }
}

/**
 * Mensaje de advertencia cuando el perfil no está completo
 * @param {Object} completionData - Datos de completitud del perfil
 * @returns {string} - Mensaje de advertencia
 */
export function getProfileWarningMessage(completionData) {
  if (completionData.canApply) {
    return ''
  }

  const { percentage, missingFields } = completionData

  return `Tu perfil está completo al ${percentage}%. Para postular a ofertas laborales, necesitas completar al menos el 80% de tu perfil.

Campos faltantes:
${missingFields.map(field => `• ${field}`).join('\n')}

Por favor, completa tu perfil en "Mi Perfil" para empezar a postular.`
}
