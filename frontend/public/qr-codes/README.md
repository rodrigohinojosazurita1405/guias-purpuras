# QR Codes para Pagos

Esta carpeta contiene los códigos QR para cada plan de pago.

## Archivos Necesarios

Coloca aquí los siguientes archivos de QR:

1. **qr-escencial.png** - QR para el Plan Escencial (35 Bs)
2. **qr-purpura.png** - QR para el Plan Púrpura (79 Bs)
3. **qr-impulso.png** - QR para el Plan Impulso Pro (169 Bs)

## Características

- **Ubicación segura**: Los QR se almacenan en la carpeta `public/`, fuera del control de versiones
- **Rutas estáticas**: Los QR se sirven como archivos estáticos desde `/qr-codes/`
- **Actualización fácil**: Solo reemplaza los archivos PNG para cambiar los QR
- **Sin necesidad de rebuild**: Los cambios en los QR se reflejan inmediatamente sin recompilar

## Configuración

La configuración de los QR está centralizada en:
```
src/config/paymentConfig.js
```

Si necesitas cambiar:
- Las rutas de los QR
- Los montos de los planes
- Las referencias de pago

...edita ese archivo.

## Seguridad

- Los QR están fuera del repositorio de código (usa `.gitignore`)
- Los QR se sirven como archivos estáticos públicos
- Las referencias de pago se generan dinámicamente (REF-XXX-TIMESTAMP-RANDOM)

## Cómo Usar

1. Genera tus QR (recomendación: usa un generador QR dinámico que apunte a tu cuenta de pagos)
2. Nombralos exactamente: `qr-escencial.png`, `qr-purpura.png`, `qr-impulso.png`
3. Cópialos a esta carpeta (`frontend/public/qr-codes/`)
4. Listo! Los QR aparecerán automáticamente en la página de pago

## Ejemplo de Estructura

```
GuiasPurpuras_V1.0/
├── frontend/
│   ├── public/
│   │   ├── qr-codes/          ← Carpeta segura para QR
│   │   │   ├── qr-escencial.png
│   │   │   ├── qr-purpura.png
│   │   │   ├── qr-impulso.png
│   │   │   └── README.md (este archivo)
│   │   └── favicon.ico
│   ├── src/
│   │   └── config/
│   │       └── paymentConfig.js  ← Configuración centralizada
```
