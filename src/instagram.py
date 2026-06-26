"""Instagram Graph API client — thin, no magic."""
import os
import httpx

BASE = "https://graph.facebook.com/v21.0"
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
PAGE_ID = os.environ.get("IG_PAGE_ID", "")
ACCOUNT_ID = os.environ.get("IG_ACCOUNT_ID", "")


def _get(path: str, **params) -> dict:
    params["access_token"] = TOKEN
    r = httpx.get(f"{BASE}/{path}", params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def _post(path: str, **data) -> dict:
    data["access_token"] = TOKEN
    r = httpx.post(f"{BASE}/{path}", data=data, timeout=20)
    r.raise_for_status()
    return r.json()


# --- PERFIL ---
def get_profile(account_id: str = "") -> dict:
    aid = account_id or ACCOUNT_ID
    return _get(aid, fields="id,name,username,followers_count,media_count,biography")


# --- POSTS ---
def get_posts(limit: int = 25) -> dict:
    return _get(f"{ACCOUNT_ID}/media",
                fields="id,caption,media_type,timestamp,like_count,comments_count",
                limit=limit)


# --- COMENTARIOS ---
def get_comments(media_id: str, limit: int = 50) -> dict:
    return _get(f"{media_id}/comments",
                fields="id,text,username,timestamp,replies{id,text,username}",
                limit=limit)


def reply_comment(comment_id: str, message: str) -> dict:
    return _post(f"{comment_id}/replies", message=message)


def post_comment(media_id: str, message: str) -> dict:
    return _post(f"{media_id}/comments", message=message)


def hide_comment(comment_id: str, hide: bool = True) -> dict:
    return _post(f"{comment_id}", is_hidden=str(hide).lower())


# --- DMs ---
def get_conversations(limit: int = 25) -> dict:
    return _get(f"{PAGE_ID}/conversations",
                platform="instagram",
                fields="id,participants,updated_time,message_count",
                limit=limit)


def get_messages(conversation_id: str, limit: int = 20) -> dict:
    return _get(f"{conversation_id}/messages",
                fields="id,message,from,created_time",
                limit=limit)


def send_dm(recipient_igsid: str, message: str) -> dict:
    """Send DM. Recipient must have messaged first within 24h."""
    return _post(f"{PAGE_ID}/messages",
                 recipient=f'{{"id":"{recipient_igsid}"}}',
                 message=f'{{"text":"{message}"}}',
                 messaging_type="RESPONSE")


# --- STORIES ---
def get_story_mentions() -> dict:
    return _get(f"{ACCOUNT_ID}/mentioned_media",
                fields="id,media_type,timestamp,mentioned_user")


def get_mentions() -> dict:
    return _get(f"{ACCOUNT_ID}/tags",
                fields="id,caption,media_type,timestamp,permalink")


# --- COMPETITOR ANALYSIS ---
def analyze_account(username: str) -> dict:
    return _get(f"{ACCOUNT_ID}",
                fields=f"business_discovery.fields(username,name,followers_count,media_count,biography,website)@{username}")


# --- HASHTAGS ---
def search_hashtag(tag: str) -> dict:
    result = _post(f"ig_hashtag_search", user_id=ACCOUNT_ID, q=tag)
    hashtag_id = result.get("data", [{}])[0].get("id")
    if not hashtag_id:
        return {"error": "hashtag not found"}
    return _get(hashtag_id, fields="id,name,media_count")


def get_hashtag_top_posts(hashtag_id: str) -> dict:
    return _get(f"{hashtag_id}/top_media",
                user_id=ACCOUNT_ID,
                fields="id,caption,like_count,comments_count,media_type,timestamp")


# --- PUBLICAR ---
def publish_image(image_url: str, caption: str) -> dict:
    container = _post(f"{ACCOUNT_ID}/media",
                      image_url=image_url, caption=caption)
    container_id = container.get("id")
    return _post(f"{ACCOUNT_ID}/media_publish", creation_id=container_id)


def get_insights(media_id: str) -> dict:
    return _get(f"{media_id}/insights",
                metric="reach,likes,comments,shares,saved")


def get_account_insights() -> dict:
    return _get(f"{ACCOUNT_ID}/insights",
                metric="reach,profile_views,accounts_engaged",
                period="day")
