#!/usr/bin/env python3
"""
ig-latam-mcp — Instagram growth MCP para creadores LATAM
Comment-to-DM · Story Reply-to-DM · Bulk replies · Competitor intel
"""
from mcp.server.fastmcp import FastMCP
from . import instagram as ig

mcp = FastMCP("ig-latam-mcp")


# ═══════════════════════════════════════════════
# PERFIL
# ═══════════════════════════════════════════════

@mcp.tool()
def get_profile(account_id: str = "") -> dict:
    """Obtiene el perfil de la cuenta Instagram Business: seguidores, bio, estadísticas."""
    return ig.get_profile(account_id)


# ═══════════════════════════════════════════════
# POSTS Y CONTENIDO
# ═══════════════════════════════════════════════

@mcp.tool()
def get_posts(limit: int = 25) -> dict:
    """Lista los posts recientes con likes y comentarios."""
    return ig.get_posts(limit)


@mcp.tool()
def publish_image(image_url: str, caption: str) -> dict:
    """Publica una imagen en Instagram con caption."""
    return ig.publish_image(image_url, caption)


@mcp.tool()
def get_post_insights(media_id: str) -> dict:
    """Métricas detalladas de un post: reach, likes, comments, shares, guardados."""
    return ig.get_insights(media_id)


@mcp.tool()
def get_account_insights() -> dict:
    """Métricas generales de la cuenta: reach diario, visitas al perfil, cuentas alcanzadas."""
    return ig.get_account_insights()


# ═══════════════════════════════════════════════
# COMENTARIOS — EL MOTOR DE CRECIMIENTO
# ═══════════════════════════════════════════════

@mcp.tool()
def get_comments(media_id: str, limit: int = 50) -> dict:
    """
    Lista todos los comentarios de un post con username y texto.
    Úsalo para identificar quién comentó y mandarles DM.
    """
    return ig.get_comments(media_id, limit)


@mcp.tool()
def reply_to_comment(comment_id: str, message: str) -> dict:
    """
    Responde a un comentario específico.
    TIP: Usa mensajes en español, personalizados por nicho LATAM.
    """
    return ig.reply_comment(comment_id, message)


@mcp.tool()
def post_comment(media_id: str, message: str) -> dict:
    """Publica un comentario en un post propio."""
    return ig.post_comment(media_id, message)


@mcp.tool()
def hide_comment(comment_id: str) -> dict:
    """Oculta un comentario negativo o spam sin borrarlo."""
    return ig.hide_comment(comment_id, hide=True)


@mcp.tool()
def bulk_reply_comments(media_id: str, reply_template: str, limit: int = 30) -> dict:
    """
    Responde en masa a comentarios no respondidos de un post.
    reply_template puede incluir {username} para personalizar.
    Retorna cuántos se respondieron y cuáles fallaron.
    """
    result = ig.get_comments(media_id, limit)
    comments = result.get("data", [])
    replied = []
    failed = []

    for comment in comments:
        # Solo responder comentarios de nivel raíz sin respuestas
        if comment.get("replies", {}).get("data"):
            continue
        username = comment.get("username", "")
        msg = reply_template.replace("{username}", f"@{username}" if username else "")
        try:
            ig.reply_comment(comment["id"], msg)
            replied.append({"id": comment["id"], "username": username})
        except Exception as e:
            failed.append({"id": comment["id"], "error": str(e)})

    return {"replied": len(replied), "failed": len(failed), "details": replied}


# ═══════════════════════════════════════════════
# DM AUTOMATION — LA KILLER FEATURE 2026
# ═══════════════════════════════════════════════

@mcp.tool()
def get_conversations(limit: int = 25) -> dict:
    """Lista todas las conversaciones DM activas con sus participantes."""
    return ig.get_conversations(limit)


@mcp.tool()
def get_messages(conversation_id: str, limit: int = 20) -> dict:
    """Lee los mensajes de una conversación DM específica."""
    return ig.get_messages(conversation_id, limit)


@mcp.tool()
def reply_dm(recipient_igsid: str, message: str) -> dict:
    """
    Responde un DM a alguien que ya te escribió (ventana de 24h).
    recipient_igsid: ID de Instagram del usuario (IGSID).
    """
    return ig.send_dm(recipient_igsid, message)


@mcp.tool()
def comment_to_dm(media_id: str, dm_message: str, max_users: int = 50) -> dict:
    """
    EL FLUJO DE CRECIMIENTO CENTRAL 2026:
    Detecta comentarios recientes en un post y manda DM a cada comentador.
    Solo funciona con usuarios que ya interactuaron contigo (dentro de 24h).

    Úsalo así:
    1. Publica un post que diga 'Comenta QUIERO y te mando el link'
    2. Ejecuta esta herramienta con el DM a enviar
    3. Cada comentador recibe el DM automáticamente

    Retorna: cuántos DMs se enviaron, cuáles fallaron.
    """
    result = ig.get_comments(media_id, max_users)
    comments = result.get("data", [])
    sent = []
    failed = []

    seen_users = set()
    for comment in comments:
        # Obtener IGSID del comentador — viene en el campo 'from' con Graph API
        from_data = comment.get("from", {})
        igsid = from_data.get("id")
        username = from_data.get("username", comment.get("username", ""))

        if not igsid or igsid in seen_users:
            continue
        seen_users.add(igsid)

        try:
            ig.send_dm(igsid, dm_message)
            sent.append({"igsid": igsid, "username": username})
        except Exception as e:
            failed.append({"username": username, "error": str(e)})

    return {
        "total_comments": len(comments),
        "dms_sent": len(sent),
        "failed": len(failed),
        "sent_to": sent
    }


@mcp.tool()
def dm_story_repliers(dm_message: str) -> dict:
    """
    Story Reply-to-DM: obtiene quién respondió tus Stories
    y les manda un DM. Conversión promedio: 15-20%.
    """
    mentions = ig.get_story_mentions()
    items = mentions.get("data", [])
    sent = []
    failed = []

    for item in items:
        igsid = item.get("from", {}).get("id")
        username = item.get("from", {}).get("username", "")
        if not igsid:
            continue
        try:
            ig.send_dm(igsid, dm_message)
            sent.append(username)
        except Exception as e:
            failed.append({"username": username, "error": str(e)})

    return {"dms_sent": len(sent), "failed": len(failed), "sent_to": sent}


# ═══════════════════════════════════════════════
# INTELIGENCIA DE COMPETENCIA Y HASHTAGS
# ═══════════════════════════════════════════════

@mcp.tool()
def analyze_competitor(username: str) -> dict:
    """
    Analiza una cuenta competidora: seguidores, posts, bio, website.
    Úsalo para benchmarking de tu nicho en LATAM.
    """
    return ig.analyze_account(username)


@mcp.tool()
def get_mentions() -> dict:
    """Obtiene posts donde te mencionaron con @. Respóndeles rápido para ganar alcance."""
    return ig.get_mentions()


@mcp.tool()
def hashtag_intel(tag: str) -> dict:
    """
    Analiza un hashtag: cuántos posts tiene, qué tan competido está.
    Úsalo para encontrar hashtags LATAM de nicho con menor competencia.
    """
    return ig.search_hashtag(tag)


@mcp.tool()
def get_hashtag_top_posts(hashtag_id: str) -> dict:
    """
    Lista los posts top de un hashtag para analizar qué contenido funciona.
    Obtén el hashtag_id primero con hashtag_intel.
    """
    return ig.get_hashtag_top_posts(hashtag_id)
