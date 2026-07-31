# AGENTS.md

Instrucciones para agentes de IA que trabajen en este repositorio. Léelo completo antes de modificar cualquier archivo.

## Visión del proyecto

**Huellitas** — Plataforma web para una organización sin fines de lucro dedicada a:

- **Rescate** de mascotas en situación de calle y reporte de mascotas perdidas.
- **Adopción responsable** con compromiso firmado en sede física y seguimiento post-adopción para garantizar un hogar seguro (evitar abandono, maltrato y venta ilícita).
- **Centro de servicios** (veterinaria, peluquería, guardería) cuyos ingresos financian el hogar de los rescatados.
- **Lista negra** de infractores por incumplimiento de las normas.
- **Comunidad** de voluntarios, donantes y colaboradores.
- **Pagos reales y donaciones** mediante pasarela de pagos.

Idioma de la interfaz y del código: **español** (nombres de modelos, vistas, plantillas, mensajes).

## Stack tecnológico

- **Python 3.14.6** / **Django 6.0.7**
- **PostgreSQL 18.4** (local) / **Neon BD** (producción)
- **django-jazzmin 3.0.5** — tema del panel admin
- **django-allauth 65.18.0** — autenticación (email + Google + Facebook)
- **django-filter 26.1** — filtros de búsqueda
- **whitenoise 6.12.0** — archivos estáticos
- **Pillow** — imágenes
- **python-decouple** — variables de entorno desde `.env`
- **Bootstrap 5.3** (CDN) en plantillas

## Estructura del proyecto

```
proyectoeth/
├── manage.py
├── requirements.txt          # Dependencias congeladas (producción, para Vercel)
├── .env                      # Variables de entorno (NO versionar)
├── .gitignore
├── requisitos/               # Archivos de dependencias organizados
│   ├── base.txt
│   ├── desarrollo.txt
│   └── produccion.txt
├── configuracion/            # Configuración del proyecto
│   ├── ajustes/
│   │   ├── __init__.py
│   │   ├── base.py           # Configuración común
│   │   ├── desarrollo.py     # PostgreSQL local, DEBUG=True
│   │   └── produccion.py     # DEBUG=False, hosts Vercel
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── aplicaciones/             # Todas las apps (nombres en español)
│   ├── pagina_principal/     # Inicio del sitio [IMPLEMENTADA]
│   ├── cuentas/              # Perfil de usuarios [IMPLEMENTADA]
│   ├── mascotas/             # Rescate, pérdida, adopción [PENDIENTE]
│   ├── servicios/            # Veterinaria, peluquería, guardería [PENDIENTE]
│   ├── chat/                 # Mensajería tiempo real [PENDIENTE]
│   ├── pagos/                # Stripe (servicios y donaciones) [PENDIENTE]
│   ├── comunidad/            # Membresías, eventos [PENDIENTE]
│   ├── seguimiento/          # Seguimiento post-adopción [PENDIENTE]
│   └── lista_negra/          # Infractores [PENDIENTE]
├── plantillas/
│   ├── base.html             # Plantilla base (Bootstrap)
│   └── aplicaciones/         # Plantillas por app
├── estaticos/                # CSS/JS propios
├── archivos_media/           # Fotos subidas (perfiles, mascotas, contratos)
└── staticfiles/              # Generado por collectstatic (no editar)
```

## Configuración

Variables en `.env` (ver `.env.example` si existe; nunca subir `.env` real):

```
SECRET_KEY=<clave>
DEBUG=True
DB_NAME=proyectoeth
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```

- PostgreSQL local usa autenticación `trust` en `C:\Program Files\PostgreSQL\18\data\pg_hba.conf`.
- Base de datos local: `proyectoeth` (creada con `createdb -U postgres proyectoeth`).
- Binarios de PostgreSQL: `C:\Program Files\PostgreSQL\18\bin` (agregar al PATH o usar ruta completa).

## Comandos de desarrollo

Todos se ejecutan desde la raíz con el entorno virtual activado:

```powershell
.\.venv\Scripts\Activate.ps1                     # Activar entorno virtual
python manage.py runserver                       # Servidor local (http://127.0.0.1:8000/)
python manage.py makemigrations                  # Crear migraciones
python manage.py migrate                         # Aplicar migraciones
python manage.py createsuperuser                 # Crear superusuario
python manage.py check                           # Verificación del sistema (SIN ERRORES)
python manage.py shell                           # Consola interactiva
```

**Verificación obligatoria antes de dar por terminada una tarea:** ejecutar `python manage.py check` y asegurar que diga `System check identified no issues`.

## Credenciales de desarrollo

| Rol | Usuario | Contraseña |
|---|---|---|
| Superusuario | `admin` | `admin123` |

## Convenciones

1. **Apps** creadas bajo `aplicaciones/` con nombres en español (`cuentas`, `mascotas`, `servicios`...).
2. **AppConfig**: cada app debe tener `name = 'aplicaciones.<nombre_app>'` en `apps.py` (no el nombre corto).
3. **Settings**: divididos en `configuracion/ajustes/{base,desarrollo,produccion}.py`. `manage.py` y `wsgi.py` apuntan a `configuracion.ajustes.desarrollo`.
4. **Plantillas**: base en `plantillas/base.html`; las de cada app en `plantillas/aplicaciones/<app>/<vista>.html` (heredan de `base.html` usando `{% extends 'base.html' %}`).
5. **Bloques de plantilla**: `{% block titulo %}`, `{% block contenido %}`, `{% block estilos %}`, `{% block scripts %}`.
6. **URLs**: cada app define su `urls.py` con `app_name = '<app>'` y se incluye desde `configuracion/urls.py` con prefijo en español (ej. `cuenta/`).
7. **Admin**: registrar modelos en `admin.py` de cada app con Jazzmin (list_display, search_fields, list_filter, inlines).
8. **Estilos**: usar las clases CSS del proyecto (`btn-verde`, `btn-ambar`, `tarjeta-hueco`, `navbar-custom`, `pie`, `hero`) y Bootstrap 5.3 vía CDN.
9. **Vistas**: funciones (function-based views) con `render(request, 'plantilla.html', contexto)`. Proteger vistas privadas con `@login_required`.
10. **Idioma**: todo el texto de interfaz, mensajes y modelos en español.
11. **NO agregar comentarios en el código** salvo que el usuario lo pida explícitamente.
12. **No hacer commit** sin autorización explícita del usuario.
13. **Nombres de modelo con verbosidad**: definir `verbose_name` y `verbose_name_plural` en cada modelo.

## Modelos implementados

### App `cuentas`
- **Perfil** (OneToOne → User): `telefono`, `direccion`, `ciudad`, `documento_identidad`, `foto`, `tipo_usuario` (adoptante/rescatista/voluntario/colaborador), `bio`, `fecha_registro`.
- Señal `post_save` crea automáticamente el `Perfil` al crear un `User`.

### App `mascotas`
- **Mascota**: `nombre`, `especie` (perro/gato/otro), `raza`, `edad` (cachorro/joven/adulto), `tamano`, `sexo`, `color`, `descripcion`, `ciudad`, `estado` (rescatado/en_adopcion/adoptado), `foto_principal`, `usuario`, `fecha_registro`.
- **FotoMascota**: `mascota` (FK → Mascota), `imagen`, `orden` (galería).
- **ReportePerdido**: `nombre`, `especie`, `raza`, `color`, `descripcion`, `foto`, `ultima_ubicacion`, `ciudad`, `latitud`, `longitud` (mapa Leaflet), `fecha_perdida`, `recompensa`, `contacto`, `estado` (perdido/encontrado), `usuario`, `fecha_registro`.
- **ReporteRescatado**: `especie`, `color`, `descripcion`, `foto`, `ciudad`, `ubicacion`, `fecha_rescate`, `estado` (rescatado/en_hogar), `usuario`, `fecha_registro`.
- **SolicitudAdopcion**: `usuario` (solicitante), `mascota`, `mensaje`, `experiencia`, `estado` (pendiente/aprobada/rechazada), `fecha_solicitud`. Protege contra solicitudes del dueño o mascotas no disponibles.

## Rutas existentes

| URL | Vista | Descripción |
|---|---|---|
| `/` | `pagina_principal:inicio` | Página de inicio |
| `/admin/` | — | Panel Jazzmin |
| `/accounts/` | — | Login/registro allauth (Google, Facebook) |
| `/cuenta/` | `cuentas:mi_perfil` | Mi perfil (requiere login) |
| `/cuenta/editar/` | `cuentas:editar_perfil` | Editar perfil (requiere login) |
| `/cuenta/<username>/` | `cuentas:perfil_publico` | Perfil público |
| `/mascotas/` | `mascotas:listado_mascotas` | Catálogo en adopción con filtros |
| `/mascotas/perdidos/` | `mascotas:listado_perdidos` | Mapa y lista de perdidos |
| `/mascotas/rescatados/` | `mascotas:listado_rescatados` | Lista de rescatados |
| `/mascotas/registrar/` | `mascotas:registrar_mascota` | Registrar mascota (login) |
| `/mascotas/perdidos/reportar/` | `mascotas:reportar_perdida` | Reportar pérdida con mapa (login) |
| `/mascotas/rescatados/reportar/` | `mascotas:reportar_rescate` | Reportar rescate (login) |
| `/mascotas/mis-mascotas/` | `mascotas:mis_mascotas` | Mis mascotas (login) |
| `/mascotas/<id>/` | `mascotas:detalle_mascota` | Detalle de mascota |
| `/mascotas/<id>/editar/` | `mascotas:editar_mascota` | Editar mascota (dueño) |
| `/mascotas/<id>/eliminar/` | `mascotas:eliminar_mascota` | Eliminar mascota (dueño) |
| `/mascotas/<id>/solicitar-adopcion/` | `mascotas:solicitar_adopcion` | Solicitud formal de adopción (login) |

## Mapa de fases (roadmap)

| Fase | App | Alcance | Estado |
|---|---|---|---|
| 1 | Configuración | Proyecto, PostgreSQL, Jazzmin, Allauth, estructura | ✅ Completada |
| 2 | cuentas | Perfil de usuario, edición, perfil público | ✅ Completada |
| 3 | mascotas | Mascota, FotoMascota, ReportePerdido, ReporteRescatado, SolicitudAdopcion, CRUD, filtros, galería | ✅ Completada |
| 4 | servicios | Servicio, Cita (veterinaria, peluquería, guardería) | ⬜ Pendiente |
| 5 | seguimiento | Seguimiento post-adopción, Visita, ListaVerificacion, alertas | ⬜ Pendiente |
| 6 | chat | Django Channels + Redis (WebSockets) | ⬜ Pendiente |
| 7 | pagos | Stripe Checkout, donaciones | ⬜ Pendiente |
| 8 | comunidad | Membresías, eventos, campañas | ⬜ Pendiente |
| 9 | lista_negra | Infractores y advertencias | ⬜ Pendiente |
| 10 | Pruebas y deploy | Tests + despliegue Vercel + Neon BD | ⬜ Pendiente |

## Despliegue (Vercel + Neon BD)

- **Hosting**: Vercel (solo funciones serverless) + **Neon BD** (PostgreSQL gratuito).
- El archivo `requirements.txt` de la raíz es autocontenido y congelado para que Vercel ejecute `pip install -r requirements.txt`.
- **Limitaciones conocidas de Vercel** que requieren alternativas al finalizar:
  - Chat tiempo real (Django Channels/WebSockets) → NO soportado; alternativa: Firebase Realtime Database o TalkJS.
  - Tareas programadas (Celery/Redis) → NO soportado; alternativa: cron-job.org llamando endpoints.
  - Subida de fotos/contratos (media local) → Alternativa: Cloudinary o Supabase Storage.
  - Almacenamiento persistente de archivos → usar servicio externo.
- En producción usar `configuracion.ajustes.produccion` (DEBUG=False, hosts `.vercel.app`).

## Reglas para agentes (resumen)

- Verificar SIEMPRE con `python manage.py check` al terminar cambios.
- No agregar comentarios al código.
- No commitear sin permiso.
- Seguir las convenciones del apartado anterior (español, estructura de apps, plantillas).
- No modificar `.env` sin confirmar con el usuario.
- Antes de instalar una librería nueva, actualizar `requirements.txt` y `requisitos/`.
- Preferir editar archivos existentes sobre crear nuevos innecesarios.
