# nanoboy-social-mcp

MCP de crecimiento en Instagram para creadores LATAM. Gratuito, open source, sin límites de precio.

## Herramientas incluidas (18 tools)

### Contenido
- `get_profile` — perfil y estadísticas
- `get_posts` — posts recientes con métricas
- `publish_image` — publica imagen con caption
- `get_post_insights` — reach, likes, shares, guardados
- `get_account_insights` — métricas de cuenta diarias

### Comentarios
- `get_comments` — lista comentarios de un post
- `reply_to_comment` — responde un comentario
- `post_comment` — publica comentario propio
- `hide_comment` — oculta spam
- `bulk_reply_comments` — responde en masa con template

### DM Automation (La killer feature)
- `get_conversations` — lista DMs activos
- `get_messages` — lee mensajes de una conversación
- `reply_dm` — responde un DM
- **`comment_to_dm`** — comenta en tu post = recibe DM automático
- **`dm_story_repliers`** — responde tu Story = recibe DM (15-20% conversión)

### Inteligencia
- `analyze_competitor` — analiza cuenta competidora
- `get_mentions` — quién te mencionó
- `hashtag_intel` — analiza un hashtag
- `get_hashtag_top_posts` — posts top de un hashtag

## Instalación

```bash
git clone https://github.com/365diascollaboration-prog/nanoboy-social-mcp
cd nanoboy-social-mcp
pip install -r requirements.txt
cp .env.example .env
# edita .env con tus tokens
```

## Configurar en Claude Code

Agrega a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nanoboy-social": {
      "command": "python",
      "args": ["-m", "nanoboy-social-mcp"],
      "cwd": "/ruta/a/nanoboy-social-mcp",
      "env": {
        "IG_ACCESS_TOKEN": "tu_token",
        "IG_PAGE_ID": "tu_page_id",
        "IG_ACCOUNT_ID": "tu_account_id"
      }
    }
  }
}
```

## El flujo de crecimiento

```
Post: "Comenta QUIERO y te mando el recurso gratis"
         ↓
  comment_to_dm(media_id, "Hola! Aquí está el link 👉 ...")
         ↓
  Cada comentador recibe DM automático
         ↓
  200 DMs/hora · 100% legal · 0% ban risk
```

## Requisitos

- Cuenta Instagram Business o Creator
- Facebook App con permisos: `instagram_manage_messages`, `instagram_manage_comments`, `instagram_content_publish`
- Access Token de larga duración (60 días, renovable)

## Por Nanoboy — 365 Días Collaboration
github.com/365diascollaboration-prog
