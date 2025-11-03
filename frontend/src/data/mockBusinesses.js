// frontend/src/data/mockBusinesses.js
// Datos de prueba FUNCIONALES

export const mockBusinesses = [
  {
    id: 1,
    slug: 'fabrica-plasticos-belen',
    name: 'Fábrica de Plásticos Belén',
    category: 'Manufactura',
    description: 'Somos una empresa líder en la fabricación de envases plásticos de alta calidad. Con más de 15 años de experiencia en el mercado boliviano.',
    logo: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=200&h=200&fit=crop',
    banner: 'https://images.unsplash.com/photo-1565688534245-05d6b5be184a?w=1200&h=400&fit=crop',
    nit: '123456789',
    phone: '4-4567890',
    email: 'info@plasticosbelen.com',
    website: 'www.plasticosbelen.com',
    city: 'Cochabamba',
    address: 'Av. América #123, Zona Sur',
    coordinates: '-17.3935, -66.1570',
    plan: 'top',
    verified: true,
    tags: ['#EnvasesPlasticos', '#Manufactura', '#Cochabamba'],
    products: [
      {
        id: 1,
        name: 'Botellas PET',
        description: 'Botellas de diferentes tamaños',
        image: 'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300&h=200&fit=crop'
      }
    ],
    createdAt: '2024-01-15'
  },
  {
    id: 2,
    slug: 'textiles-andinos',
    name: 'Textiles Andinos S.A.',
    category: 'Textil',
    description: 'Producción de textiles tradicionales bolivianos utilizando técnicas ancestrales. Trabajamos con comunidades locales.',
    logo: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=200&h=200&fit=crop',
    banner: 'https://images.unsplash.com/photo-1618453292507-4959ece6429e?w=1200&h=400&fit=crop',
    nit: '987654321',
    phone: '2-2234567',
    email: 'contacto@textilesandinos.com',
    website: 'www.textilesandinos.com',
    city: 'La Paz',
    address: 'Calle Sagárnaga #456',
    coordinates: '-16.5000, -68.1500',
    plan: 'destacado',
    verified: true,
    tags: ['#Textiles', '#Artesanía', '#LaPaz'],
    products: [
      {
        id: 1,
        name: 'Aguayos Tradicionales',
        description: 'Tejidos artesanales',
        image: 'https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=300&h=200&fit=crop'
      }
    ],
    createdAt: '2024-02-20'
  }
]

// Función para obtener negocio por slug
export const getBusinessBySlug = (slug) => {
  return mockBusinesses.find(b => b.slug === slug)
}

// Función para filtrar negocios
export const filterBusinesses = (filters = {}) => {
  let result = [...mockBusinesses]

  if (filters.search) {
    const searchLower = filters.search.toLowerCase()
    result = result.filter(b =>
      b.name.toLowerCase().includes(searchLower) ||
      b.description.toLowerCase().includes(searchLower) ||
      b.tags?.some(tag => tag.toLowerCase().includes(searchLower))
    )
  }

  if (filters.category && filters.category !== 'Todas') {
    result = result.filter(b => b.category === filters.category)
  }

  if (filters.city && filters.city !== 'Todas') {
    result = result.filter(b => b.city === filters.city)
  }

  if (filters.plan && filters.plan !== 'Todos') {
    result = result.filter(b =>
      b.plan.toLowerCase() === filters.plan.toLowerCase()
    )
  }

  // Ordenar por plan
  const planOrder = { top: 0, destacado: 1, sugerido: 2, basico: 3 }
  return result.sort((a, b) => planOrder[a.plan] - planOrder[b.plan])
}