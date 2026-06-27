# ig-latam-mcp

**Controla Instagram desde Claude Code.** MCP de automatización y crecimiento para creadores LATAM — gratuito, open source, 100% Graph API oficial.

Construido por [Nanoboy — 365 Días Collaboration](https://github.com/365diascollaboration-prog)

---

## ¿Qué puedes hacer con esto?

- Responder comentarios en masa con un solo comando
- Mandar DM automático a todos los que comenten en tu post
- Analizar cuentas competidoras y hashtags de tu nicho
- Publicar contenido, ver métricas y gestionar tu cuenta
- Todo desde Claude Code, en español, sin pagar herramientas de terceros

---

## Las 19 herramientas incluidas

### Perfil y contenido
| Tool | ¿Qué hace? |
|------|-----------|
| `get_profile` | Tu perfil: seguidores, bio, estadísticas |
| `get_posts` | Posts recientes con likes y comentarios |
| `publish_image` | Publica una imagen con caption |
| `get_post_insights` | Métricas de un post: reach, guardados, shares |
| `get_account_insights` | Métricas diarias de toda la cuenta |

### Comentarios
| Tool | ¿Qué hace? |
|------|-----------|
| `get_comments` | Lista comentarios de un post con usernames |
| `reply_to_comment` | Responde un comentario específico |
| `post_comment` | Publica un comentario en tu propio post |
| `hide_comment` | Oculta spam sin borrarlo |
| `bulk_reply_comments` | Responde en masa con template `{username}` |

### DM Automation ⚡ (la killer feature)
| Tool | ¿Qué hace? |
|------|-----------|
| `get_conversations` | Lista todas tus conversaciones DM activas |
| `get_messages` | Lee mensajes de una conversación |
| `reply_dm` | Responde un DM a alguien que ya te escribió |
| `comment_to_dm` | **Manda DM automático a todos los que comentaron** |
| `dm_story_repliers` | Manda DM a todos los que respondieron tu Story |

### Inteligencia de mercado
| Tool | ¿Qué hace? |
|------|-----------|
| `analyze_competitor` | Analiza seguidores, bio y posts de una cuenta rival |
| `get_mentions` | Ve quién te mencionó con @ para responder rápido |
| `hashtag_intel` | Qué tan competido está un hashtag |
| `get_hashtag_top_posts` | Posts top de un hashtag para ver qué funciona |

---

## El flujo de crecimiento

```
Publicas: "Comenta QUIERO y te mando el recurso gratis"
              ↓
    comment_to_dm(media_id, "Hola! Aquí está 👉 ...")
              ↓
    Cada comentador recibe su DM automáticamente
              ↓
    200 DMs/hora · 100% Meta oficial · 0% riesgo de ban
```

---

## Instalación

```bash
git clone https://github.com/365diascollaboration-prog/ig-latam-mcp
cd ig-latam-mcp
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus credenciales (ver guía abajo)
```

---

## Guía de credenciales paso a paso

Necesitas dos cosas: una **Facebook App** y un **Access Token**. Sigue estos pasos:

### Paso 1 — Crear tu Facebook App

1. Ve a [developers.facebook.com](https://developers.facebook.com) e inicia sesión
2. Clic en **"Mis apps"** → **"Crear app"**
3. Selecciona tipo: **"Otros"** → **"Empresa"**
4. Ponle un nombre (ej: `mi-ig-mcp`) y guarda

### Paso 2 — Activar Instagram Graph API

1. Dentro de tu app ve a **"Agregar productos"**
2. Busca **"Instagram Graph API"** y haz clic en **"Configurar"**
3. En el panel izquierdo entra a **"Instagram Graph API"** → **"Configuración"**

### Paso 3 — Conectar tu cuenta de Instagram

> Tu cuenta debe ser **Business** o **Creator** (no personal)

1. Ve a **"Herramientas"** → **"Explorador de la API Graph"**
2. Selecciona tu app en el menú desplegable
3. Clic en **"Generar token de acceso de usuario"**
4. Activa estos permisos:
   - `instagram_basic`
   - `instagram_manage_messages`
   - `instagram_manage_comments`
   - `instagram_content_publish`
   - `pages_show_list`
5. Clic en **"Generar token"** y autoriza tu cuenta

### Paso 4 — Obtener token de larga duración (60 días)

El token generado dura solo 1 hora. Para extenderlo a 60 días ejecuta:

```bash
curl "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_id=TU_APP_ID&client_secret=TU_APP_SECRET&access_token=TU_TOKEN_CORTO"
```

Copia el `access_token` que te devuelve.

### Paso 5 — Obtener tu Account ID

```bash
curl "https://graph.instagram.com/v21.0/me?fields=id,username&access_token=TU_TOKEN_LARGO"
```

El campo `id` que devuelve es tu `IG_ACCOUNT_ID`.

### Paso 6 — Configurar el .env

```env
IG_ACCESS_TOKEN=tu_token_de_larga_duracion
IG_ACCOUNT_ID=tu_account_id
```

### Paso 7 — Activar tu app en modo LIVE

1. En tu app de Meta Developers ve al panel principal
2. En la parte superior verás **"Modo: Desarrollo"** → cámbialo a **"Activo (Live)"**
3. Acepta las políticas

> En modo Desarrollo solo funciona con cuentas de testers. En modo Live funciona con cualquier usuario.

---

## Configurar en Claude Code

Agrega esto a tu `~/.claude.json` (o usa `claude mcp add`):

```json
{
  "mcpServers": {
    "ig-latam": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/ruta/a/ig-latam-mcp",
      "env": {
        "IG_ACCESS_TOKEN": "tu_token",
        "IG_ACCOUNT_ID": "tu_account_id"
      }
    }
  }
}
```

O desde la terminal:

```bash
claude mcp add ig-latam --scope user -- python -m src.server
```

---

## Requisitos

- Python 3.10+
- Cuenta Instagram **Business** o **Creator**
- Facebook App con los permisos listados arriba
- Claude Code instalado

---

## ¿No quieres hacer todo esto tú solo?

Si tienes una cuenta de Instagram y quieres este sistema funcionando sin tocar código, puedo hacerlo por ti.

**Contacto:** 365diascollaboration@gmail.com
**Canal YouTube:** [@365collaboration](https://www.youtube.com/@365collaboration)

---

*Construido con ❤️ para creadores de LATAM — código abierto, sin límites, sin suscripciones.*
