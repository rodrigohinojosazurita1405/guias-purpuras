# Media Upload Debug Report

## Issue Identified
User reported: "por que no esta conectando con la db ya que no se copia las fotos en la carpeta media"
(Images are not being copied to the media folder)

## Root Cause Found
**The media folder did not exist** on the filesystem!

```
EXPECTED: d:/Proyectos Django/GuiasPurpuras_V1.0/media/
STATUS: ❌ MISSING
```

## Solution Applied

### 1. Created Media Directory Structure
Created the following folders:
```
media/
├── .gitkeep                    (to track folder in git)
├── company_logos/              (for company logo uploads)
├── company_banners/            (for company banner uploads)
└── profile_photos/             (for user profile photos)
```

Command executed:
```bash
mkdir -p media/company_logos media/company_banners media/profile_photos
touch media/.gitkeep
```

### 2. Verified Backend Configuration

**Django Settings (core/settings.py)**:
```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Absolute path to media directory
```
✅ CORRECT

**URL Configuration (core/urls.py)**:
```python
# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
✅ CORRECT - Media files will be served from /media/ endpoint

### 3. Database Models (profiles/models.py)

**UserProfile Model**:
```python
profilePhoto = models.ImageField(
    upload_to='profile_photos/',
    blank=True,
    null=True,
    verbose_name="Foto de Perfil"
)
```
✅ CORRECT

**CompanyProfile Model**:
```python
logo = models.ImageField(
    upload_to='company_logos/',
    blank=True,
    null=True,
    verbose_name="Logo de Empresa"
)

banner = models.ImageField(
    upload_to='company_banners/',
    blank=True,
    null=True,
    verbose_name="Banner de Empresa"
)
```
✅ CORRECT

### 4. Backend Views (profiles/views.py)

**update_company_profile** (Lines 508-656):
- Handles PATCH requests to `/api/profiles/company/<company_id>/`
- Accepts FormData with optional `logo` and `banner` files
- Validates file size: logo (5MB max), banner (10MB max)
- Removes old files before saving new ones
- Returns complete company profile with media URLs
✅ CORRECT

**upload_company_logo** (Lines 921-988):
- Handles POST/PATCH to `/api/profiles/company/<company_id>/logo`
- Validates file type (JPEG, PNG, GIF, WEBP)
- Validates file size (5MB max)
- Saves logo file to media/company_logos/
✅ CORRECT

**delete_company_logo** (Lines 994-1049):
- Handles PATCH to `/api/profiles/company/<company_id>/logo/delete`
- Removes logo file and sets model field to NULL
- Returns updated company profile
✅ CORRECT

**delete_company_banner** (Lines 1055+):
- Handles PATCH to `/api/profiles/company/<company_id>/banner/delete`
- Removes banner file and sets model field to NULL
- Returns updated company profile
✅ CORRECT

### 5. Frontend Store (useCompanyStore.js)

**uploadCompanyLogo** (Lines 234-281):
```javascript
const uploadCompanyLogo = async (companyId, logoFile) => {
  const formData = new FormData()
  formData.append('logo', logoFile)

  const response = await fetch(`${API_BASE}/profiles/company/${companyId}/`, {
    method: 'PATCH',
    body: formData,
    headers: { 'Authorization': `Bearer ${jwtToken}` }
  })

  // Updates currentCompany.value with response data
  currentCompany.value = { ...currentCompany.value, ...data.profile }
}
```
✅ CORRECT

**uploadCompanyBanner** (Lines 286-333):
- Same pattern as uploadCompanyLogo
✅ CORRECT

**deleteCompanyLogo** (Lines 369-400):
**deleteCompanyBanner** (Lines 405-436):
✅ CORRECT

### 6. Frontend Component (CompanyMediaUpload.vue)

**Logo Upload Handler** (Lines 261-285):
- Calls `companyStore.uploadCompanyLogo()` in isolation
- Only sends logo file, never sends banner
- Prevents images from disappearing
✅ CORRECT

**Banner Upload Handler** (Lines 353-377):
- Calls `companyStore.uploadCompanyBanner()` in isolation
- Only sends banner file, never sends logo
- Prevents images from disappearing
✅ CORRECT

## What Was Wrong Before

The old implementation (CompanyLogoUpload.vue) was:
1. Mixing logo and banner in a single FormData object
2. Sending `{ logo: file, banner: null }` which DELETED the banner
3. Sending `{ logo: null, banner: file }` which DELETED the logo
4. Not following the proven AvatarUpload.vue pattern

This is why the user said: "al presionar guardar logo se borra todo lo subido y muestra como en blanco"

## Current Status

✅ Media folder structure created
✅ Backend properly configured
✅ Models correctly defined
✅ Frontend components rewritten to match working pattern
✅ Separate upload methods for logo and banner

## How to Test

1. Open company profile edit
2. Select and upload logo → click "Guardar Logo"
   - Check: `media/company_logos/` folder has the file
   - Check: Logo displays in the component
3. Select and upload banner → click "Guardar Banner"
   - Check: `media/company_banners/` folder has the file
   - Check: Banner displays in the component
4. Try deleting logo → verify banner still exists
5. Try deleting banner → verify logo still exists
6. Reload the page (F5) → verify both images persist

## File Paths for Reference

- **Models**: [profiles/models.py](../profiles/models.py#L46-L117)
- **Views**: [profiles/views.py](../profiles/views.py#L508-L656)
- **URLs**: [profiles/urls.py](../profiles/urls.py)
- **Store**: [frontend/src/stores/useCompanyStore.js](../frontend/src/stores/useCompanyStore.js#L234-L333)
- **Component**: [frontend/src/components/Profile/CompanyMediaUpload.vue](../frontend/src/components/Profile/CompanyMediaUpload.vue)
- **Media Directory**: `media/` (now created with .gitkeep)
