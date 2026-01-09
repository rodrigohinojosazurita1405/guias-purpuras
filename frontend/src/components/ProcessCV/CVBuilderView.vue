<!-- frontend/src/views/Dashboard/CVBuilderView.vue -->
<template>
  <div class="cv-builder-view">
    <div class="cv-builder-container">
      <!-- Header -->
      <div class="cv-builder-header">
        <button class="back-button" @click="handleBack">
          <va-icon name="arrow_back" size="20px" />
          Volver a Mis CVs
        </button>
        <h1 class="cv-builder-title">{{ isEditing ? 'Editar CV' : 'Crear CV Profesional Formato Harvard' }}</h1>
        <p class="cv-builder-subtitle">Completa la información para crear tu currículum profesional</p>
      </div>

      <!-- Steps Indicator -->
      <CVStepsIndicator :currentStep="currentStep" :steps="cvSteps" />

      <!-- Form Content -->
      <div class="cv-builder-content">
        <!-- Step 0: Información Personal + Perfil Profesional -->
        <div v-if="currentStep === 0" class="step-content">
          <h2 class="step-heading">Información Personal y Perfil</h2>
          <p class="step-description">Proporciona tus datos de contacto y un resumen profesional</p>

          <!-- Información Personal -->
          <div class="subsection-divider">
            <h3 class="subsection-title">Datos de Contacto</h3>
          </div>
          <div class="form-grid">
            <va-input
              v-model="cvFormData.personalInfo.fullName"
              label="Nombre Completo"
              placeholder="Ej: Juan Carlos Pérez López"
              required-mark
              class="full-width"
              @blur="cvFormData.personalInfo.fullName = capitalizeWords(cvFormData.personalInfo.fullName)"
            />
            <va-input
              v-model="cvFormData.personalInfo.title"
              label="Título Profesional / Cargo Objetivo"
              placeholder="Ej: Ingeniero de Software, Analista de Datos, Diseñador UX/UI"
              class="full-width"
              @blur="cvFormData.personalInfo.title = capitalizeWords(cvFormData.personalInfo.title)"
            />
            <va-input
              v-model="cvFormData.personalInfo.phone"
              label="Teléfono"
              placeholder="+591 XXXXXXXX"
              required-mark
            />
            <va-input
              v-model="cvFormData.personalInfo.email"
              label="Correo Profesional"
              placeholder="correo.profesional@ejemplo.com"
              type="email"
              required-mark
            />
            <va-input
              v-model="cvFormData.personalInfo.location"
              label="Ciudad y País"
              placeholder="La Paz, Bolivia"
              @blur="cvFormData.personalInfo.location = capitalizeWords(cvFormData.personalInfo.location)"
            />
            <va-input
              v-model="cvFormData.personalInfo.linkedin"
              label="LinkedIn"
              placeholder="linkedin.com/in/usuario"
            />
            <va-input
              v-model="cvFormData.personalInfo.portfolio"
              label="Portafolio / Sitio Web"
              placeholder="www.misitioweb.com"
            />
          </div>

          <!-- Perfil Profesional -->
          <div class="subsection-divider">
            <h3 class="subsection-title">Perfil Profesional (Summary Statement)</h3>
          </div>
          <va-textarea
            v-model="cvFormData.professionalProfile"
            placeholder="Resumen ejecutivo de 3-4 líneas destacando su experiencia, competencias clave y logros cuantificables. Use verbos de acción y enfoque en resultados medibles. Ej: 'Gerente de Ventas con 7+ años aumentando ingresos en sectores B2B. Logré incremento de 45% en ventas regionales mediante implementación de estrategias de retención de clientes. Especializado en análisis de mercado, negociación y desarrollo de equipos de alto rendimiento.'"
            :min-rows="6"
            :max-rows="10"
            counter
            :max-length="500"
          />
          <p class="field-hint"><strong>Formato Harvard:</strong> Use verbos de acción (Logré, Incrementé, Desarrollé) + resultados cuantificables (%, números, tiempo).</p>
        </div>

        <!-- Step 1: Experiencia Profesional -->
        <div v-if="currentStep === 1" class="step-content">
          <h2 class="step-heading">Experiencia Profesional (Work Experience)</h2>
          <p class="step-description" style="margin-bottom: 1.5rem;">
            <strong>IMPORTANTE - Cronología inversa:</strong> Comience por su trabajo actual o más reciente y continúe hacia atrás en el tiempo.
            <br>
            <strong>Formato Harvard:</strong> Verbo de acción + Resultado cuantificable + Método/Contexto.
          </p>

          <div class="step-header-actions">
            <button class="add-btn" @click="addExperience">
              <va-icon name="add" size="small" />
              Agregar Experiencia
            </button>
          </div>

          <div v-if="cvFormData.experience.length === 0" class="empty-state">
            <va-icon name="work_outline" size="3rem" color="#D1D5DB" />
            <p>No ha agregado experiencia profesional</p>
          </div>

          <div v-for="(exp, index) in cvFormData.experience" :key="index" class="accordion-item">
            <div class="accordion-header" @click="toggleExperience(index)">
              <div class="accordion-header-left">
                <span class="mini-number">{{ index + 1 }}</span>
                <span class="accordion-title">
                  {{ exp.position || 'Nueva experiencia' }}
                  <span v-if="exp.company" class="accordion-subtitle">- {{ exp.company }}</span>
                </span>
              </div>
              <div class="accordion-header-right">
                <button
                  class="remove-btn-mini"
                  @click.stop="removeExperience(index)"
                  title="Eliminar"
                >
                  <va-icon name="close" size="12px" />
                </button>
                <va-icon
                  :name="expandedExpIndex === index ? 'expand_less' : 'expand_more'"
                  size="20px"
                  class="accordion-icon"
                />
              </div>
            </div>
            <va-collapse :model-value="expandedExpIndex === index">
              <div class="accordion-content">
                <div class="form-grid">
              <va-input v-model="exp.startYear" label="Año Inicio" placeholder="YYYY" />
              <va-input v-model="exp.endYear" label="Año Fin" placeholder="YYYY o 'Actual'" :disabled="exp.current" />

              <div class="switch-wrapper">
                <label class="custom-switch">
                  <input type="checkbox" v-model="exp.current" />
                  <span class="custom-switch-slider"></span>
                </label>
                <span class="switch-text">Estado:</span>
                <span class="divider">|</span>
                <span class="switch-status" :class="{ active: exp.current }">
                  {{ exp.current ? 'Trabajo Actual' : 'Finalizado' }}
                </span>
              </div>

              <va-input v-model="exp.position" label="Cargo" placeholder="Ej: Gerente de Ventas Regional" class="full-width" @blur="exp.position = capitalizeWords(exp.position)" />
              <va-input v-model="exp.company" label="Empresa" placeholder="Nombre de la empresa" class="full-width" @blur="exp.company = capitalizeWords(exp.company)" />

              <!-- Referencias Laborales -->
              <div class="references-section full-width">
                <label class="references-label">
                  <va-icon name="person" size="small" />
                  Referencias Laborales (Opcional pero recomendado)
                </label>
                <div class="references-grid">
                  <va-input
                    v-model="exp.supervisorName"
                    label="Nombre del Supervisor/Jefe"
                    placeholder="Ej: Juan Pérez"
                    @blur="exp.supervisorName = capitalizeWords(exp.supervisorName)"
                  />
                  <va-input
                    v-model="exp.supervisorPhone"
                    label="Teléfono de Referencia"
                    placeholder="Ej: +591 12345678"
                  />
                </div>
              </div>

              <div class="achievements-section full-width">
                <label class="achievements-label">Logros Cuantificables (3-4 bullet points - Formato Harvard)</label>
                <p class="achievement-hint">Cada logro debe seguir: VERBO DE ACCIÓN + RESULTADO MEDIBLE + MÉTODO. Ej: "Incrementé ventas en 35% mediante implementación de CRM"</p>
                <div v-for="(achievement, achIndex) in exp.achievements" :key="achIndex" class="achievement-input-wrapper">
                  <va-input
                    v-model="exp.achievements[achIndex]"
                    :placeholder="`• Verbo + Resultado + Método: 'Reduje costos operativos en 25% optimizando procesos de compras'`"
                    @blur="exp.achievements[achIndex] = capitalizeFirstLetter(exp.achievements[achIndex])"
                  >
                    <template #append>
                      <button v-if="exp.achievements.length > 1" class="remove-achievement-btn" @click="removeAchievement(index, achIndex)">
                        <va-icon name="close" size="small" />
                      </button>
                    </template>
                  </va-input>
                </div>
                <button v-if="exp.achievements.length < 4" class="add-achievement-btn" @click="addAchievement(index)">
                  <va-icon name="add" size="small" />
                  Agregar logro
                </button>
              </div>
                </div>
              </div>
            </va-collapse>
          </div>
        </div>

        <!-- Step 2: Educación + Habilidades -->
        <div v-if="currentStep === 2" class="step-content">
          <!-- Educación -->
          <h2 class="step-heading">Educación (Education)</h2>
          <p class="step-description" style="margin-bottom: 1.5rem;">
            <strong>IMPORTANTE - Cronología inversa:</strong> Comience por su formación más reciente (último título/curso/diplomado) y continúe hacia atrás en el tiempo.
            <br>
            Incluya título, institución, años, y honores/logros relevantes (menciones honoríficas, becas, proyectos destacados).
          </p>

          <div class="step-header-actions">
            <button class="add-btn" @click="addEducation">
              <va-icon name="add" size="small" />
              Agregar Educación
            </button>
          </div>

          <div v-if="cvFormData.education.length === 0" class="empty-state">
            <va-icon name="school" size="3rem" color="#D1D5DB" />
            <p>No ha agregado formación académica</p>
          </div>

          <div v-for="(edu, index) in cvFormData.education" :key="index" class="accordion-item">
            <div class="accordion-header" @click="toggleEducation(index)">
              <div class="accordion-header-left">
                <span class="mini-number">{{ index + 1 }}</span>
                <span class="accordion-title">
                  {{ edu.degree || 'Nueva educación' }}
                  <span v-if="edu.institution" class="accordion-subtitle">- {{ edu.institution }}</span>
                </span>
              </div>
              <div class="accordion-header-right">
                <button
                  class="remove-btn-mini"
                  @click.stop="removeEducation(index)"
                  title="Eliminar"
                >
                  <va-icon name="close" size="12px" />
                </button>
                <va-icon
                  :name="expandedEduIndex === index ? 'expand_less' : 'expand_more'"
                  size="20px"
                  class="accordion-icon"
                />
              </div>
            </div>
            <va-collapse :model-value="expandedEduIndex === index">
              <div class="accordion-content">
                <div class="form-grid">
                  <va-input v-model="edu.startYear" label="Año Inicio" placeholder="YYYY" />
                  <va-input v-model="edu.endYear" label="Año Fin" placeholder="YYYY o 'Actual'" />
                  <va-input v-model="edu.degree" label="Título Obtenido" placeholder="Ej: Licenciatura en Administración de Empresas" class="full-width" @blur="edu.degree = capitalizeWords(edu.degree)" />
                  <va-input v-model="edu.institution" label="Institución" placeholder="Nombre de la universidad/instituto" class="full-width" @blur="edu.institution = capitalizeWords(edu.institution)" />
                  <va-textarea v-model="edu.achievements" label="Logros o Detalles Relevantes" placeholder="Ej: Graduado con mención honorífica" :min-rows="2" class="full-width" @blur="edu.achievements = capitalizeFirstLetter(edu.achievements)" />
                </div>
              </div>
            </va-collapse>
          </div>

          <!-- Habilidades -->
          <div style="margin-top: 3rem; padding-top: 2rem; border-top: 2px solid #E5E7EB;">
            <h2 class="step-heading" style="margin-bottom: 1rem;">Habilidades (Skills)</h2>
            <p class="step-description" style="margin-bottom: 2rem; line-height: 1.8;">
              <strong>Formato Harvard:</strong> Priorice habilidades relevantes para el puesto objetivo.
              <br><br>
              Liste primero las técnicas/específicas, luego las transferibles o Blandas.
            </p>
          </div>

          <!-- Habilidades Técnicas -->
          <div class="skills-subsection">
            <label class="subsection-label">Habilidades Técnicas (Technical/Hard Skills)</label>
            <p class="skills-hint">Software, herramientas, sistemas, certificaciones técnicas específicas de su industria</p>
            <div class="skills-input-wrapper">
              <va-input
                v-model="newTechnicalSkill"
                placeholder="Ej: Excel Avanzado, SAP, CRM Salesforce"
                @keyup.enter="addTechnicalSkill"
              >
                <template #append>
                  <button class="add-skill-btn" @click="addTechnicalSkill" :disabled="!newTechnicalSkill.trim()">
                    <va-icon name="add" size="small" />
                  </button>
                </template>
              </va-input>
            </div>
            <div v-if="cvFormData.technicalSkills.length > 0" class="skills-list">
              <div v-for="(skill, index) in cvFormData.technicalSkills" :key="index" class="skill-tag">
                <span>{{ skill }}</span>
                <button @click="removeTechnicalSkill(index)" class="remove-skill-btn">
                  <va-icon name="close" size="small" />
                </button>
              </div>
            </div>
          </div>

          <!-- Habilidades Blandas -->
          <div class="skills-subsection">
            <label class="subsection-label">Habilidades Transferibles / Blandas (Soft/Transferable Skills)</label>
            <p class="skills-hint">Competencias interpersonales y de gestión aplicables a diversos contextos laborales</p>
            <div class="skills-input-wrapper">
              <va-input
                v-model="newSoftSkill"
                placeholder="Ej: Liderazgo, Comunicación efectiva"
                @keyup.enter="addSoftSkill"
              >
                <template #append>
                  <button class="add-skill-btn" @click="addSoftSkill" :disabled="!newSoftSkill.trim()">
                    <va-icon name="add" size="small" />
                  </button>
                </template>
              </va-input>
            </div>
            <div v-if="cvFormData.softSkills.length > 0" class="skills-list">
              <div v-for="(skill, index) in cvFormData.softSkills" :key="index" class="skill-tag soft">
                <span>{{ skill }}</span>
                <button @click="removeSoftSkill(index)" class="remove-skill-btn">
                  <va-icon name="close" size="small" />
                </button>
              </div>
            </div>
          </div>

          <!-- Certificaciones, Idiomas, Proyectos -->
          <div class="additional-sections">
            <!-- Certificaciones -->
            <div class="subsection-card">
              <div class="subsection-header">
                <h3><va-icon name="verified" size="small" /> Certificaciones</h3>
                <button class="add-btn-small" @click="addCertification">
                  <va-icon name="add" size="small" />
                </button>
              </div>
              <div v-if="cvFormData.certifications.length === 0" class="mini-empty-state">
                <p>Sin certificaciones</p>
              </div>
              <div v-for="(cert, index) in cvFormData.certifications" :key="index" class="accordion-item">
                <div class="accordion-header" @click="toggleCertification(index)">
                  <div class="accordion-header-left">
                    <span class="mini-number">{{ index + 1 }}</span>
                    <span class="accordion-title">
                      {{ cert.name || 'Nueva certificación' }}
                      <span v-if="cert.institution" class="accordion-subtitle">- {{ cert.institution }}</span>
                    </span>
                  </div>
                  <div class="accordion-header-right">
                    <button
                      class="remove-btn-mini"
                      @click.stop="removeCertification(index)"
                      title="Eliminar"
                    >
                      <va-icon name="close" size="12px" />
                    </button>
                    <va-icon
                      :name="expandedCertIndex === index ? 'expand_less' : 'expand_more'"
                      size="20px"
                      class="accordion-icon"
                    />
                  </div>
                </div>
                <va-collapse :model-value="expandedCertIndex === index">
                  <div class="accordion-content">
                    <div class="form-grid-mini">
                      <va-input v-model="cert.year" label="Año" placeholder="YYYY" />
                      <va-input v-model="cert.name" label="Certificación" placeholder="Nombre" class="full-width" @blur="cert.name = capitalizeWords(cert.name)" />
                      <va-input v-model="cert.institution" label="Institución" placeholder="Institución" class="full-width" @blur="cert.institution = capitalizeWords(cert.institution)" />
                    </div>
                  </div>
                </va-collapse>
              </div>
            </div>

            <!-- Idiomas -->
            <div class="subsection-card">
              <div class="subsection-header">
                <h3><va-icon name="language" size="small" /> Idiomas</h3>
                <button class="add-btn-small" @click="addLanguage">
                  <va-icon name="add" size="small" />
                </button>
              </div>
              <div v-if="cvFormData.languages.length === 0" class="mini-empty-state">
                <p>Sin idiomas</p>
              </div>
              <div v-for="(lang, index) in cvFormData.languages" :key="index" class="accordion-item-ultra-compact">
                <div class="accordion-header-compact" @click="toggleLanguage(index)">
                  <div class="accordion-header-left">
                    <span class="mini-number-small">{{ index + 1 }}</span>
                    <span class="accordion-title-compact">
                      {{ lang.name || 'Nuevo idioma' }}
                      <span v-if="lang.level" class="level-badge">{{ lang.level }}</span>
                    </span>
                  </div>
                  <div class="accordion-header-right">
                    <button
                      class="remove-btn-mini"
                      @click.stop="removeLanguage(index)"
                      title="Eliminar"
                    >
                      <va-icon name="close" size="12px" />
                    </button>
                    <va-icon
                      :name="expandedLangIndex === index ? 'expand_less' : 'expand_more'"
                      size="18px"
                      class="accordion-icon"
                    />
                  </div>
                </div>
                <va-collapse :model-value="expandedLangIndex === index">
                  <div class="accordion-body-compact">
                    <va-input
                      v-model="lang.name"
                      placeholder="Ej: Español"
                      size="small"
                      @blur="lang.name = capitalizeWords(lang.name)"
                    />
                    <select v-model="lang.level" class="select-compact-inline">
                      <option value="" disabled>Nivel</option>
                      <option value="Básico">Básico</option>
                      <option value="Intermedio">Intermedio</option>
                      <option value="Avanzado">Avanzado</option>
                      <option value="Nativo / Bilingüe">Nativo / Bilingüe</option>
                    </select>
                  </div>
                </va-collapse>
              </div>
            </div>

            <!-- Proyectos -->
            <div class="subsection-card">
              <div class="subsection-header">
                <h3><va-icon name="article" size="small" /> Proyectos (Opcional)</h3>
                <button class="add-btn-small" @click="addProject">
                  <va-icon name="add" size="small" />
                </button>
              </div>
              <div v-if="cvFormData.projects.length === 0" class="mini-empty-state">
                <p>Sin proyectos</p>
              </div>
              <div v-for="(project, index) in cvFormData.projects" :key="index" class="accordion-item">
                <div class="accordion-header" @click="toggleProject(index)">
                  <div class="accordion-header-left">
                    <span class="mini-number">{{ index + 1 }}</span>
                    <span class="accordion-title">
                      {{ project.name || 'Nuevo proyecto' }}
                    </span>
                  </div>
                  <div class="accordion-header-right">
                    <button
                      class="remove-btn-mini"
                      @click.stop="removeProject(index)"
                      title="Eliminar"
                    >
                      <va-icon name="close" size="12px" />
                    </button>
                    <va-icon
                      :name="expandedProjectIndex === index ? 'expand_less' : 'expand_more'"
                      size="20px"
                      class="accordion-icon"
                    />
                  </div>
                </div>
                <va-collapse :model-value="expandedProjectIndex === index">
                  <div class="accordion-content">
                    <div class="form-grid-mini">
                      <va-input v-model="project.year" label="Año" placeholder="YYYY" />
                      <va-input v-model="project.name" label="Proyecto" placeholder="Nombre" class="full-width" @blur="project.name = capitalizeWords(project.name)" />
                      <va-textarea v-model="project.description" label="Descripción" placeholder="Impacto y resultados" :min-rows="2" class="full-width" @blur="project.description = capitalizeFirstLetter(project.description)" />
                    </div>
                  </div>
                </va-collapse>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3: Vista Previa -->
        <div v-if="currentStep === 3" class="step-content">
          <h2 class="step-heading centered">Vista Previa - Revisa tu CV antes de guardar</h2>

          <!-- CV Preview Container - Estilo impreso -->
          <div class="cv-preview-paper">
            <!-- Header: Nombre y Contacto -->
            <div class="cv-header">
              <h1 class="cv-name">{{ cvFormData.personalInfo.fullName || 'TU NOMBRE' }}</h1>
              <p class="cv-title">{{ cvFormData.personalInfo.title || 'Título Profesional' }}</p>
              <p class="cv-contact">
                <template v-if="cvFormData.personalInfo.phone">
                  {{ cvFormData.personalInfo.phone }}
                  <span class="cv-dot">•</span>
                </template>
                <template v-if="cvFormData.personalInfo.email">
                  {{ cvFormData.personalInfo.email }}
                </template>
                <template v-if="cvFormData.personalInfo.location">
                  <span class="cv-dot">•</span>
                  {{ cvFormData.personalInfo.location }}
                </template>
              </p>
              <p class="cv-contact" v-if="cvFormData.personalInfo.linkedin || cvFormData.personalInfo.portfolio">
                <template v-if="cvFormData.personalInfo.linkedin">
                  {{ cvFormData.personalInfo.linkedin }}
                </template>
                <template v-if="cvFormData.personalInfo.portfolio">
                  <span class="cv-dot" v-if="cvFormData.personalInfo.linkedin">•</span>
                  {{ cvFormData.personalInfo.portfolio }}
                </template>
              </p>
            </div>

            <!-- Summary / Perfil Profesional -->
            <div class="cv-section" v-if="cvFormData.professionalProfile">
              <h2 class="cv-section-title">Perfil Profesional</h2>
              <p class="cv-summary">{{ cvFormData.professionalProfile }}</p>
            </div>

            <!-- Skills -->
            <div class="cv-section" v-if="cvFormData.technicalSkills.length > 0 || cvFormData.softSkills.length > 0">
              <h2 class="cv-section-title">Habilidades</h2>
              <div class="cv-skills-group" v-if="cvFormData.technicalSkills.length > 0">
                <span class="cv-skills-label">Técnicas:</span>
                <span class="cv-skills-list">{{ cvFormData.technicalSkills.join(' · ') }}</span>
              </div>
              <div class="cv-skills-group" v-if="cvFormData.softSkills.length > 0">
                <span class="cv-skills-label">Blandas:</span>
                <span class="cv-skills-list">{{ cvFormData.softSkills.join(' · ') }}</span>
              </div>
            </div>

            <!-- Experience -->
            <div class="cv-section" v-if="cvFormData.experience.length > 0">
              <h2 class="cv-section-title">Experiencia</h2>
              <div v-for="(exp, i) in cvFormData.experience" :key="i" class="cv-experience-item">
                <div class="cv-exp-header">
                  <span class="cv-exp-company">{{ exp.company }}</span>
                  <span class="cv-exp-location">{{ exp.location }}</span>
                </div>
                <div class="cv-exp-role">
                  <span class="cv-exp-position">{{ exp.position }}</span>
                  <span class="cv-exp-dates">{{ exp.startYear }} - {{ exp.current ? 'Actual' : exp.endYear }}</span>
                </div>
                <ul class="cv-exp-bullets" v-if="exp.achievements && exp.achievements.some(a => a?.trim())">
                  <li v-for="(achievement, idx) in exp.achievements.filter(a => a?.trim())" :key="idx">
                    {{ achievement }}
                  </li>
                </ul>
                <div class="cv-reference" v-if="exp.supervisorName || exp.supervisorPhone">
                  <span class="cv-reference-label">Referencia:</span>
                  <span v-if="exp.supervisorName">{{ exp.supervisorName }}</span>
                  <span v-if="exp.supervisorPhone"> • {{ exp.supervisorPhone }}</span>
                </div>
              </div>
            </div>

            <!-- Education -->
            <div class="cv-section" v-if="cvFormData.education.length > 0">
              <h2 class="cv-section-title">Educación</h2>
              <div v-for="(edu, i) in cvFormData.education" :key="i" class="cv-education-item">
                <div class="cv-edu-header">
                  <span class="cv-edu-institution">{{ edu.institution }}</span>
                  <span class="cv-edu-location">{{ edu.location }}</span>
                </div>
                <div class="cv-edu-degree">
                  <span class="cv-edu-title">{{ edu.degree }}</span>
                  <span class="cv-edu-dates">{{ edu.startYear }} - {{ edu.endYear }}</span>
                </div>
              </div>
            </div>

            <!-- Certifications -->
            <div class="cv-section" v-if="cvFormData.certifications.length > 0">
              <h2 class="cv-section-title">Cursos y Certificaciones</h2>
              <div v-for="(cert, i) in cvFormData.certifications" :key="i" class="cv-cert-item">
                {{ cert.name }} — <strong>{{ cert.institution }}</strong>, {{ cert.year }}
              </div>
            </div>

            <!-- Languages -->
            <div class="cv-section" v-if="cvFormData.languages.length > 0">
              <h2 class="cv-section-title">Idiomas</h2>
              <div class="cv-languages-list">
                <span v-for="(lang, i) in cvFormData.languages" :key="i" class="cv-language-item">
                  <strong>{{ lang.name }}:</strong> {{ lang.level }}<span v-if="i < cvFormData.languages.length - 1"> · </span>
                </span>
              </div>
            </div>

            <!-- Projects -->
            <div class="cv-section" v-if="cvFormData.projects.length > 0">
              <h2 class="cv-section-title">Proyectos</h2>
              <div v-for="(proj, i) in cvFormData.projects" :key="i" class="cv-project-item">
                <div class="cv-project-header">
                  <span class="cv-project-name">{{ proj.name }}</span>
                  <span class="cv-project-year">{{ proj.year }}</span>
                </div>
                <p class="cv-project-desc" v-if="proj.description">{{ proj.description }}</p>
              </div>
            </div>
          </div>

          <!-- Watermark -->
          <div class="cv-watermark">
            Powered by Guías Púrpuras Bolivia
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="cv-builder-actions">
        <div class="spacer"></div>

        <button
          v-if="currentStep > 0"
          class="action-btn secondary-btn"
          @click="previousStep"
        >
          <va-icon name="arrow_back" size="18px" />
          Atrás
        </button>

        <button
          v-if="currentStep < cvSteps.length - 1"
          class="action-btn primary-btn"
          @click="nextStep"
        >
          Siguiente
          <va-icon name="arrow_forward" size="18px" />
        </button>

        <button
          v-else
          class="action-btn save-btn"
          @click="saveCV"
          :disabled="!isValidCV"
        >
          <va-icon name="save" size="18px" />
          Guardar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast, useModal } from 'vuestic-ui'
import CVStepsIndicator from './CVStepsIndicator.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { init: initToast } = useToast()
const { confirm } = useModal()

const DRAFT_KEY = 'cv_builder_draft'

// State
const currentStep = ref(0)
const cvFormData = ref({
  personalInfo: {
    fullName: '',
    title: '',
    phone: '',
    email: '',
    location: '',
    linkedin: '',
    portfolio: ''
  },
  professionalProfile: '',
  education: [],
  experience: [],
  technicalSkills: [],
  softSkills: [],
  certifications: [],
  languages: [],
  projects: []
})

const isEditing = ref(false)
const editingCVId = ref(null)

// Skills state
const newTechnicalSkill = ref('')
const newSoftSkill = ref('')

// Accordion state for certifications, languages, projects, experience, and education
const expandedCertIndex = ref(null)
const expandedLangIndex = ref(null)
const expandedProjectIndex = ref(null)
const expandedExpIndex = ref(null)
const expandedEduIndex = ref(null)

// Capitalization functions
const capitalizeWords = (str) => {
  if (!str) return ''
  return str
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const capitalizeFirstLetter = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

// Steps configuration
const cvSteps = [
  { name: 'Información y Perfil', description: 'Datos personales y resumen' },
  { name: 'Experiencia', description: 'Historial laboral' },
  { name: 'Educación y Habilidades', description: 'Formación y competencias' },
  { name: 'Vista Previa', description: 'Revisión final' }
]

// Computed
const isValidCV = computed(() => {
  const info = cvFormData.value?.personalInfo
  if (!info) return false

  return (
    info.fullName?.trim().length > 0 &&
    info.email?.trim().length > 0 &&
    info.phone?.trim().length > 0
  )
})

// Validación por pasos
const canProceedToNextStep = computed(() => {
  switch (currentStep.value) {
    case 0: // Información Personal + Perfil
      return (
        cvFormData.value.personalInfo.fullName?.trim() &&
        cvFormData.value.personalInfo.email?.trim() &&
        cvFormData.value.personalInfo.phone?.trim() &&
        cvFormData.value.professionalProfile?.trim()
      )
    case 1: // Experiencia
      // Requerido: Al menos 1 experiencia profesional con al menos 1 logro
      if (cvFormData.value.experience.length === 0) return false
      return cvFormData.value.experience.every(exp => {
        const hasBasicInfo = exp.position?.trim() && exp.company?.trim()
        const hasAtLeastOneAchievement = exp.achievements?.some(ach => ach?.trim())
        return hasBasicInfo && hasAtLeastOneAchievement
      })
    case 2: // Educación, Habilidades, Certificaciones e Idiomas
      // Validar educación: mínimo 1
      if (cvFormData.value.education.length === 0) return false
      const educationValid = cvFormData.value.education.every(edu =>
        edu.degree?.trim() && edu.institution?.trim()
      )

      // Validar habilidades técnicas: mínimo 3
      const technicalSkillsValid = cvFormData.value.technicalSkills.length >= 3

      // Validar habilidades blandas: mínimo 3
      const softSkillsValid = cvFormData.value.softSkills.length >= 3

      // Validar certificaciones: mínimo 2
      if (cvFormData.value.certifications.length < 2) return false
      const certificationsValid = cvFormData.value.certifications.every(cert =>
        cert.name?.trim() && cert.institution?.trim()
      )

      // Validar idiomas: mínimo 1
      if (cvFormData.value.languages.length < 1) return false
      const languagesValid = cvFormData.value.languages.every(lang =>
        lang.name?.trim() && lang.level?.trim()
      )

      return educationValid && technicalSkillsValid && softSkillsValid && certificationsValid && languagesValid
    default:
      return true
  }
})

// Auto-save to localStorage
watch(cvFormData, (newData) => {
  if (!isEditing.value) {
    saveDraft(newData)
  }
}, { deep: true })

const saveDraft = (data) => {
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify({
      data,
      currentStep: currentStep.value,
      timestamp: Date.now()
    }))
  } catch (error) {
    console.error('Error saving draft:', error)
  }
}

const loadDraft = () => {
  try {
    const draft = localStorage.getItem(DRAFT_KEY)
    if (draft) {
      const { data, currentStep: savedStep, timestamp } = JSON.parse(draft)

      // Solo cargar si el borrador tiene menos de 7 días
      const sevenDaysInMs = 7 * 24 * 60 * 60 * 1000
      if (Date.now() - timestamp < sevenDaysInMs) {
        cvFormData.value = data
        currentStep.value = savedStep

        initToast({
          message: 'Se restauró tu borrador guardado',
          color: 'info',
          duration: 3000
        })
      } else {
        // Borrador muy antiguo, eliminarlo
        localStorage.removeItem(DRAFT_KEY)
      }
    }
  } catch (error) {
    console.error('Error loading draft:', error)
  }
}

const clearDraft = () => {
  localStorage.removeItem(DRAFT_KEY)
}

// Methods
const nextStep = () => {
  if (!canProceedToNextStep.value) {
    let message = ''
    switch (currentStep.value) {
      case 0:
        message = 'Por favor completa: Nombre completo, Email, Teléfono y Perfil Profesional antes de continuar'
        break
      case 1:
        if (cvFormData.value.experience.length === 0) {
          message = 'Por favor agrega al menos 1 experiencia profesional para continuar'
        } else {
          const hasIncompleteBasicInfo = cvFormData.value.experience.some(exp => !exp.position?.trim() || !exp.company?.trim())
          const hasNoAchievements = cvFormData.value.experience.some(exp => !exp.achievements?.some(ach => ach?.trim()))

          if (hasIncompleteBasicInfo) {
            message = 'Por favor completa el Cargo y Empresa en todas las experiencias'
          } else if (hasNoAchievements) {
            message = 'Por favor agrega al menos 1 logro cuantificable en cada experiencia'
          }
        }
        break
      case 2:
        const errors = []

        if (cvFormData.value.education.length === 0) {
          errors.push('al menos 1 educación')
        } else if (cvFormData.value.education.some(edu => !edu.degree?.trim() || !edu.institution?.trim())) {
          errors.push('completa el Título e Institución en todas las educaciones')
        }

        if (cvFormData.value.technicalSkills.length < 3) {
          errors.push(`${cvFormData.value.technicalSkills.length}/3 habilidades técnicas`)
        }

        if (cvFormData.value.softSkills.length < 3) {
          errors.push(`${cvFormData.value.softSkills.length}/3 habilidades blandas`)
        }

        if (cvFormData.value.certifications.length < 2) {
          errors.push(`${cvFormData.value.certifications.length}/2 certificaciones`)
        } else if (cvFormData.value.certifications.some(cert => !cert.name?.trim() || !cert.institution?.trim())) {
          errors.push('completa Nombre e Institución en todas las certificaciones')
        }

        if (cvFormData.value.languages.length < 1) {
          errors.push('al menos 1 idioma')
        } else if (cvFormData.value.languages.some(lang => !lang.name?.trim() || !lang.level?.trim())) {
          errors.push('completa Idioma y Nivel en todos los idiomas')
        }

        message = errors.length > 0
          ? `Por favor agrega: ${errors.join(', ')}`
          : 'Completa todos los campos requeridos'
        break
    }

    initToast({
      message,
      color: 'warning',
      duration: 4000
    })
    return
  }

  if (currentStep.value < cvSteps.length - 1) {
    currentStep.value++
    saveDraft(cvFormData.value)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
    saveDraft(cvFormData.value)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const handleBack = async () => {
  const hasDraft = localStorage.getItem(DRAFT_KEY)

  if (hasDraft) {
    const agreed = await confirm({
      title: 'Salir del CV Builder',
      message: 'Tienes un borrador guardado. ¿Deseas salir sin finalizar?\n\nPodrás continuar más tarde desde donde lo dejaste.',
      okText: 'Salir',
      cancelText: 'Continuar editando',
      size: 'small',
      maxWidth: '400px'
    })

    if (agreed) {
      router.push('/dashboard/cv')
    }
  } else {
    router.push('/dashboard/cv')
  }
}

// Education functions
const addEducation = () => {
  cvFormData.value.education.push({
    startYear: '',
    endYear: '',
    degree: '',
    institution: '',
    achievements: ''
  })
  // Auto-expand the newly added education
  expandedEduIndex.value = cvFormData.value.education.length - 1
}

const removeEducation = async (index) => {
  const edu = cvFormData.value.education[index]
  const eduTitle = edu.degree || edu.institution || 'esta educación'

  const agreed = await confirm({
    title: 'Eliminar Educación',
    message: `¿Estás seguro de que deseas eliminar "${eduTitle}"?\n\nEsta acción no se puede deshacer.`,
    okText: 'Eliminar',
    cancelText: 'Cancelar',
    size: 'small',
    maxWidth: '380px'
  })

  if (!agreed) return

  cvFormData.value.education.splice(index, 1)
  // Reset expanded index if we removed the expanded item
  if (expandedEduIndex.value === index) {
    expandedEduIndex.value = null
  } else if (expandedEduIndex.value > index) {
    expandedEduIndex.value -= 1
  }
}

const toggleEducation = (index) => {
  expandedEduIndex.value = expandedEduIndex.value === index ? null : index
}

// Experience functions
const addExperience = () => {
  cvFormData.value.experience.push({
    startYear: '',
    endYear: '',
    current: false,
    position: '',
    company: '',
    supervisorName: '',
    supervisorPhone: '',
    achievements: ['', '', '']
  })
  // Auto-expand the newly added experience
  expandedExpIndex.value = cvFormData.value.experience.length - 1
}

const removeExperience = async (index) => {
  const exp = cvFormData.value.experience[index]
  const expTitle = exp.position || exp.company || 'esta experiencia'

  const agreed = await confirm({
    title: 'Eliminar Experiencia Laboral',
    message: `¿Estás seguro de que deseas eliminar "${expTitle}"?\n\nEsta acción no se puede deshacer.`,
    okText: 'Eliminar',
    cancelText: 'Cancelar',
    size: 'small',
    maxWidth: '380px'
  })

  if (!agreed) return

  cvFormData.value.experience.splice(index, 1)
  // Reset expanded index if we removed the expanded item
  if (expandedExpIndex.value === index) {
    expandedExpIndex.value = null
  } else if (expandedExpIndex.value > index) {
    expandedExpIndex.value -= 1
  }
}

const toggleExperience = (index) => {
  expandedExpIndex.value = expandedExpIndex.value === index ? null : index
}

const addAchievement = (expIndex) => {
  if (cvFormData.value.experience[expIndex].achievements.length < 4) {
    cvFormData.value.experience[expIndex].achievements.push('')
  }
}

const removeAchievement = (expIndex, achIndex) => {
  cvFormData.value.experience[expIndex].achievements.splice(achIndex, 1)
}

// Technical Skills functions
const addTechnicalSkill = () => {
  const skill = newTechnicalSkill.value.trim()
  if (skill && !cvFormData.value.technicalSkills.includes(skill)) {
    cvFormData.value.technicalSkills.push(capitalizeWords(skill))
    newTechnicalSkill.value = ''
  }
}

const removeTechnicalSkill = (index) => {
  cvFormData.value.technicalSkills.splice(index, 1)
}

// Soft Skills functions
const addSoftSkill = () => {
  const skill = newSoftSkill.value.trim()
  if (skill && !cvFormData.value.softSkills.includes(skill)) {
    cvFormData.value.softSkills.push(capitalizeWords(skill))
    newSoftSkill.value = ''
  }
}

const removeSoftSkill = (index) => {
  cvFormData.value.softSkills.splice(index, 1)
}

// Certifications functions
const addCertification = () => {
  cvFormData.value.certifications.push({
    year: '',
    name: '',
    institution: ''
  })
  // Auto-expand the newly added certification
  expandedCertIndex.value = cvFormData.value.certifications.length - 1
}

const removeCertification = (index) => {
  cvFormData.value.certifications.splice(index, 1)
  // Reset expanded index if we removed the expanded item
  if (expandedCertIndex.value === index) {
    expandedCertIndex.value = null
  } else if (expandedCertIndex.value > index) {
    expandedCertIndex.value -= 1
  }
}

const toggleCertification = (index) => {
  expandedCertIndex.value = expandedCertIndex.value === index ? null : index
}

// Languages functions
const addLanguage = () => {
  cvFormData.value.languages.push({
    name: '',
    level: 'Básico'
  })
  // Auto-expand the newly added language
  expandedLangIndex.value = cvFormData.value.languages.length - 1
}

const removeLanguage = (index) => {
  cvFormData.value.languages.splice(index, 1)
  // Reset expanded index if we removed the expanded item
  if (expandedLangIndex.value === index) {
    expandedLangIndex.value = null
  } else if (expandedLangIndex.value > index) {
    expandedLangIndex.value -= 1
  }
}

const toggleLanguage = (index) => {
  expandedLangIndex.value = expandedLangIndex.value === index ? null : index
}

// Projects functions
const addProject = () => {
  cvFormData.value.projects.push({
    year: '',
    name: '',
    description: ''
  })
  // Auto-expand the newly added project
  expandedProjectIndex.value = cvFormData.value.projects.length - 1
}

const removeProject = (index) => {
  cvFormData.value.projects.splice(index, 1)
  // Reset expanded index if we removed the expanded item
  if (expandedProjectIndex.value === index) {
    expandedProjectIndex.value = null
  } else if (expandedProjectIndex.value > index) {
    expandedProjectIndex.value -= 1
  }
}

const toggleProject = (index) => {
  expandedProjectIndex.value = expandedProjectIndex.value === index ? null : index
}

const saveCV = async () => {
  if (!isValidCV.value) {
    initToast({
      message: 'Por favor completa la información requerida: Nombre completo, Email, Teléfono y Perfil Profesional',
      color: 'warning',
      duration: 4000
    })
    return
  }

  try {
    const cvName = `CV - ${cvFormData.value.personalInfo.fullName}`
    let cvId = null

    if (isEditing.value && editingCVId.value) {
      // Update existing CV
      const response = await fetch(`http://localhost:8000/api/cvs/${editingCVId.value}/update/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: cvName,
          cv_data: cvFormData.value
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'No se pudo actualizar el CV. Por favor, intenta nuevamente.')
      }

      cvId = editingCVId.value

      initToast({
        message: 'CV guardado. Generando PDF...',
        color: 'info',
        duration: 2000
      })
    } else {
      // Create new CV
      const response = await fetch('http://localhost:8000/api/cvs/save/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          cv_type: 'created',
          name: cvName,
          cv_data: cvFormData.value
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'No se pudo guardar el CV. Por favor, intenta nuevamente.')
      }

      const data = await response.json()
      cvId = data.cv.id

      initToast({
        message: 'CV creado. Generando PDF...',
        color: 'info',
        duration: 2000
      })
    }

    // Generar PDF
    const pdfResponse = await fetch(`http://localhost:8000/api/cvs/${cvId}/generate-pdf/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!pdfResponse.ok) {
      const errorData = await pdfResponse.json()
      console.error('Error generando PDF:', errorData)
      // No lanzar error, solo advertir
      initToast({
        message: 'CV guardado pero hubo un error al generar el PDF',
        color: 'warning',
        duration: 4000
      })
    } else {
      initToast({
        message: isEditing.value ? 'CV actualizado y PDF generado exitosamente' : 'CV creado y PDF generado exitosamente',
        color: 'success',
        duration: 3000
      })
    }

    clearDraft() // Limpiar borrador al guardar exitosamente

    // Redirect back to CVs list
    router.push('/dashboard/cv')
  } catch (error) {
    console.error('Error saving CV:', error)
    initToast({
      message: error.message || 'Ocurrió un error al procesar tu solicitud',
      color: 'danger',
      duration: 4000
    })
  }
}

// Load CV if editing or load draft
onMounted(async () => {
  const cvId = route.query.edit
  if (cvId) {
    isEditing.value = true
    editingCVId.value = cvId

    try {
      const response = await fetch(`http://localhost:8000/api/cvs/${cvId}/`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      if (!response.ok) {
        throw new Error('No se pudo cargar el CV para editar')
      }

      const data = await response.json()
      cvFormData.value = data.cv.cv_data || cvFormData.value
    } catch (error) {
      console.error('Error loading CV:', error)
      initToast({
        message: error.message || 'No se pudo cargar el CV. Por favor, intenta nuevamente.',
        color: 'danger',
        duration: 4000
      })
    }
  } else {
    // Si no está editando, intentar cargar borrador
    loadDraft()
  }
})
</script>

<style scoped>
.cv-builder-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
  padding: 2rem 1rem;
}

.cv-builder-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.cv-builder-header {
  text-align: center;
  margin-bottom: 2rem;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  color: #6b7280;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 1.5rem;
}

.back-button:hover {
  border-color: #7c3aed;
  color: #7c3aed;
  transform: translateX(-4px);
}

.cv-builder-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cv-builder-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
}

/* Content */
.cv-builder-content {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  margin-bottom: 2rem;
}

/* Actions */
.cv-builder-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.spacer {
  flex: 1;
}

.action-btn {
  flex: 1;
  max-width: 250px;
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 15px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.primary-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
  margin-left: auto;
}

.primary-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
}

.secondary-btn {
  background: white;
  color: #6b7280;
  border: 2px solid #e5e7eb;
}

.secondary-btn:hover {
  border-color: #7c3aed;
  color: #7c3aed;
}

.save-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
  margin-left: auto;
}

.save-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Step Content */
.step-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step-heading {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.step-heading.centered {
  text-align: center;
  margin-bottom: 1.5rem;
}

.step-description {
  font-size: 1rem;
  color: #6b7280;
  margin: -0.5rem 0 0;
}

.subsection-divider {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.75rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #E5E7EB;
}

.subsection-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.step-header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.step-header-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.field-hint {
  font-size: 0.875rem;
  color: #6b7280;
  margin: -0.5rem 0 0;
  font-style: italic;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.form-grid :deep(.va-input-wrapper__field),
.form-grid :deep(.va-input-wrapper__text),
.form-grid :deep(input),
.form-grid :deep(textarea) {
  background-color: white !important;
}

.full-width {
  grid-column: 1 / -1;
}

/* Buttons */
.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: white;
  border: 2px solid #7c3aed;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #7c3aed;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn:hover {
  background: #7c3aed;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.2);
}

.add-btn-small {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  background: white;
  border: 1.5px solid #7c3aed;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #7c3aed;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn-small:hover {
  background: #7c3aed;
  color: white;
}

/* Item Cards */
.item-card {
  background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.item-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.item-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 28px;
  padding: 0 0.5rem;
  background: #7c3aed;
  color: white;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 700;
}

.remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: #fef2f2;
  border-color: #fca5a5;
  color: #dc2626;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  background: #f9fafb;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
}

.empty-state p {
  margin: 0.75rem 0 0;
  font-size: 0.9375rem;
  color: #9ca3af;
  font-weight: 500;
}

/* Switch */
.switch-wrapper {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.125rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.switch-text {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #6b7280;
  margin-left: 0.5rem;
}

.divider {
  color: #d1d5db;
  margin: 0 0.375rem;
}

.switch-status {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #6b7280;
  transition: color 0.2s ease;
}

.switch-status.active {
  color: #10b981;
}

.custom-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 22px;
  cursor: pointer;
}

.custom-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.custom-switch-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #d1d5db;
  border-radius: 22px;
  transition: all 0.3s ease;
}

.custom-switch-slider::before {
  content: "";
  position: absolute;
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.custom-switch input:checked + .custom-switch-slider {
  background-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.custom-switch input:checked + .custom-switch-slider::before {
  transform: translateX(22px);
}

/* Achievements */
/* References Section */
.references-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.references-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.references-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.achievements-section {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
  padding: 1.125rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.achievements-label {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.achievement-hint {
  font-size: 0.8125rem;
  color: #7c3aed;
  margin: 0 0 0.75rem 0;
  padding: 0.5rem 0.75rem;
  background: rgba(124, 58, 237, 0.05);
  border-left: 3px solid #7c3aed;
  border-radius: 4px;
  font-style: italic;
}

.achievement-input-wrapper {
  display: flex;
  gap: 0.5rem;
}

.remove-achievement-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-achievement-btn:hover {
  color: #dc2626;
}

.add-achievement-btn {
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-achievement-btn:hover {
  background: #f9fafb;
  border-color: #7c3aed;
  color: #7c3aed;
}

/* Skills */
.skills-subsection {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
  padding: 1.125rem;
  background: #f9fafb;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.subsection-label {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.skills-hint {
  font-size: 0.8125rem;
  color: #6b7280;
  margin: 0 0 0.75rem 0;
  font-style: italic;
}

.skills-input-wrapper {
  margin-bottom: 0.5rem;
}

.add-skill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #7c3aed;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-skill-btn:hover:not(:disabled) {
  background: #6d28d9;
  transform: scale(1.05);
}

.add-skill-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  background: white;
  border: 2px solid #7c3aed;
  border-radius: 20px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #7c3aed;
  transition: all 0.2s ease;
}

.skill-tag:hover {
  background: #f3f4f6;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.1);
}

.skill-tag.soft {
  border-color: #10b981;
  color: #10b981;
}

.remove-skill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: currentColor;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0.7;
}

.remove-skill-btn:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.08);
}

/* Additional Sections */
.additional-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.subsection-card {
  background: #fafafa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1rem;
}

.subsection-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.875rem;
}

.subsection-header h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.mini-empty-state {
  padding: 1.5rem;
  text-align: center;
  background: white;
  border: 1px dashed #d1d5db;
  border-radius: 8px;
}

.mini-empty-state p {
  margin: 0;
  font-size: 0.875rem;
  color: #9ca3af;
}

.mini-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.875rem;
  margin-bottom: 0.75rem;
}

.mini-item:last-child {
  margin-bottom: 0;
}

/* Accordion styles */
.accordion-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  overflow: hidden;
  transition: all 0.2s ease;
}

.accordion-item:last-child {
  margin-bottom: 0;
}

.accordion-item:hover {
  border-color: #d1d5db;
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
}

.accordion-header:hover {
  background-color: #f9fafb;
}

.accordion-header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}

.accordion-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.accordion-subtitle {
  font-weight: 400;
  color: #6b7280;
  margin-left: 0.25rem;
}

.accordion-header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.accordion-icon {
  color: #9ca3af;
  transition: transform 0.2s ease;
}

.accordion-content {
  padding: 0 0.875rem 0.875rem 0.875rem;
}

/* Ultra compact accordion for languages */
.accordion-item-ultra-compact {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  overflow: hidden;
  transition: all 0.2s ease;
}

.accordion-item-ultra-compact:last-child {
  margin-bottom: 0;
}

.accordion-item-ultra-compact:hover {
  border-color: #d1d5db;
}

.accordion-header-compact {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  min-height: 36px;
}

.accordion-header-compact:hover {
  background-color: #f9fafb;
}

.accordion-title-compact {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #374151;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mini-number-small {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 0.25rem;
  background: #7c3aed;
  color: white;
  border-radius: 4px;
  font-size: 0.6875rem;
  font-weight: 700;
}

.level-badge {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.accordion-body-compact {
  padding: 0.5rem 0.75rem 0.75rem 0.75rem;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.accordion-body-compact .va-input-wrapper {
  flex: 1;
}

.select-compact-inline {
  flex: 1;
  padding: 0.5rem 1.75rem 0.5rem 0.75rem;
  font-size: 0.8125rem;
  color: #1f2937;
  background-color: white;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'%3E%3Cpath fill='%236b7280' d='M5 7.5L1 3.5h8z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  height: 32px;
}

.select-compact-inline:hover {
  border-color: #9ca3af;
}

.select-compact-inline:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1);
}

.mini-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.mini-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.375rem;
  background: #7c3aed;
  color: white;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
}

.remove-btn-mini {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-btn-mini:hover {
  background: #fef2f2;
  border-color: #fca5a5;
  color: #dc2626;
}

.form-grid-mini {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 0.75rem;
}

/* Select */
.select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.select-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.custom-select {
  width: 100%;
  padding: 0.625rem 2rem 0.625rem 0.875rem;
  font-size: 1rem;
  color: #1f2937;
  background-color: white;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.custom-select:hover {
  border-color: #9ca3af;
}

.custom-select:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

/* Preview */
/* CV Preview - Estilo impreso profesional */
.cv-preview-paper {
  width: 8.5in;
  min-height: 11in;
  max-width: 850px;
  margin: 0 auto;
  background: white;
  padding: 0.75in;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.5;
  color: #1a1a1a;
  position: relative;
  display: flex;
  flex-direction: column;
}

/* Watermark */
.cv-watermark {
  text-align: right;
  margin-top: auto;
  padding-top: 1.5rem;
  font-size: 9px;
  color: rgba(124, 58, 237, 0.35);
  font-weight: 500;
  letter-spacing: 0.5px;
  font-style: italic;
}

/* Header */
.cv-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
}

.cv-name {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin: 0 0 0.25rem 0;
  color: #000;
  text-transform: uppercase;
}

.cv-title {
  font-size: 1rem;
  color: #4a4a4a;
  margin: 0 0 0.5rem 0;
  font-weight: 400;
}

.cv-contact {
  font-size: 0.875rem;
  color: #4a4a4a;
  margin: 0;
}

.cv-dot {
  margin: 0 0.5rem;
}

/* Secciones */
.cv-section {
  margin-bottom: 1.75rem;
}

.cv-section-title {
  font-size: 1.125rem;
  font-weight: 700;
  text-align: center;
  text-transform: capitalize;
  margin: 0 0 0.75rem 0;
  padding-bottom: 0.375rem;
  border-bottom: 2px solid #000;
  color: #000;
}

/* Summary */
.cv-summary {
  font-size: 0.9rem;
  line-height: 1.6;
  text-align: justify;
  margin: 0;
  color: #2a2a2a;
}

/* Skills */
.cv-skills-group {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.cv-skills-label {
  font-weight: 600;
  color: #2a2a2a;
}

.cv-skills-list {
  color: #4a4a4a;
  margin-left: 0.25rem;
}

/* Experience */
.cv-experience-item {
  margin-bottom: 1.25rem;
}

.cv-experience-item:last-child {
  margin-bottom: 0;
}

.cv-exp-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.125rem;
}

.cv-exp-company {
  font-weight: 700;
  font-size: 0.95rem;
  color: #000;
}

.cv-exp-location {
  font-size: 0.875rem;
  color: #4a4a4a;
  text-align: right;
}

.cv-exp-role {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
}

.cv-exp-position {
  font-weight: 600;
  font-style: italic;
  font-size: 0.9rem;
  color: #2a2a2a;
}

.cv-exp-dates {
  font-size: 0.875rem;
  color: #4a4a4a;
  text-align: right;
}

.cv-exp-bullets {
  margin: 0;
  padding-left: 1.25rem;
  font-size: 0.875rem;
  color: #2a2a2a;
  line-height: 1.6;
}

.cv-exp-bullets li {
  margin-bottom: 0.25rem;
}

.cv-reference {
  margin-top: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #f9fafb;
  border-left: 3px solid #7c3aed;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #4b5563;
  display: flex;
  gap: 0.375rem;
  align-items: center;
}

.cv-reference-label {
  font-weight: 600;
  color: #374151;
}

/* Education */
.cv-education-item {
  margin-bottom: 0.875rem;
}

.cv-education-item:last-child {
  margin-bottom: 0;
}

.cv-edu-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.cv-edu-institution {
  font-weight: 700;
  font-size: 0.95rem;
  color: #000;
}

.cv-edu-location {
  font-size: 0.875rem;
  color: #4a4a4a;
  text-align: right;
}

.cv-edu-degree {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.9rem;
}

.cv-edu-title {
  color: #2a2a2a;
}

.cv-edu-dates {
  font-size: 0.875rem;
  color: #4a4a4a;
  text-align: right;
}

/* Certifications */
.cv-cert-item {
  font-size: 0.875rem;
  margin-bottom: 0.375rem;
  color: #2a2a2a;
  line-height: 1.5;
}

/* Languages */
.cv-languages-list {
  font-size: 0.9rem;
  color: #2a2a2a;
}

.cv-language-item strong {
  color: #000;
}

/* Projects */
.cv-project-item {
  margin-bottom: 1rem;
}

.cv-project-item:last-child {
  margin-bottom: 0;
}

.cv-project-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.25rem;
}

.cv-project-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: #000;
}

.cv-project-year {
  font-size: 0.875rem;
  color: #4a4a4a;
}

.cv-project-desc {
  font-size: 0.875rem;
  color: #2a2a2a;
  margin: 0;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 768px) {
  .cv-builder-view {
    padding: 1rem 0.5rem;
  }

  .cv-builder-title {
    font-size: 1.75rem;
  }

  .cv-builder-subtitle {
    font-size: 1rem;
  }

  .cv-builder-content {
    padding: 1.5rem;
  }

  .cv-builder-actions {
    flex-direction: column;
    padding: 1rem;
  }

  .action-btn {
    max-width: 100%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: 1;
  }

  .step-header-section {
    flex-direction: column;
    align-items: stretch;
  }

  .add-btn {
    width: 100%;
    justify-content: center;
  }

  .additional-sections {
    grid-template-columns: 1fr;
  }

  .step-heading {
    font-size: 1.5rem;
  }

  /* CV Preview responsive */
  .cv-preview-paper {
    padding: 2rem 1.5rem;
  }

  .cv-name {
    font-size: 1.5rem;
  }

  .cv-contact {
    font-size: 0.8rem;
  }

  .cv-exp-header,
  .cv-exp-role,
  .cv-edu-header,
  .cv-edu-degree,
  .cv-project-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .cv-exp-location,
  .cv-exp-dates,
  .cv-edu-location,
  .cv-edu-dates,
  .cv-project-year {
    text-align: left;
    margin-top: 0.125rem;
  }
}

/* ========================================
   ESTILOS DE IMPRESIÓN - Tamaño Carta
   ======================================== */
@media print {
  /* Configuración de página tamaño Carta (Letter) */
  @page {
    size: letter; /* 8.5in x 11in */
    margin: 0.75in; /* Márgenes estándar */
  }

  /* Ajustar el contenedor del CV para impresión */
  .cv-preview-paper {
    max-width: 100%;
    padding: 0;
    margin: 0;
    box-shadow: none;
    background: white;
  }

  /* Evitar saltos de página dentro de elementos */
  .cv-section,
  .cv-exp-item,
  .cv-edu-item,
  .cv-project-item {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Permitir salto de página después de secciones si es necesario */
  .cv-section {
    page-break-after: auto;
    break-after: auto;
  }

  /* Evitar que el encabezado se repita en cada página */
  .cv-header {
    page-break-after: avoid;
    break-after: avoid;
  }

  /* Asegurar que los títulos de sección no queden huérfanos */
  .cv-section-title {
    page-break-after: avoid;
    break-after: avoid;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Ocultar elementos que no deben imprimirse */
  .cv-builder-header,
  .cv-builder-footer,
  .step-navigation,
  button,
  .back-button {
    display: none !important;
  }

  /* Ajustar tamaños de fuente para impresión */
  body {
    font-size: 11pt;
    line-height: 1.4;
  }

  .cv-name {
    font-size: 18pt;
  }

  .cv-title {
    font-size: 12pt;
  }

  .cv-section-title {
    font-size: 13pt;
  }

  .cv-contact {
    font-size: 10pt;
  }
}
</style>
