"""
Contact App — Discord Webhook Utility
Sends a rich embed notification to a Discord channel whenever a verified
contact message is submitted through the VASTIK website.

Required environment variables (set in .env / Railway):
    DISCORD_WEBHOOK_URL       — the full Discord webhook URL
    DISCORD_THUMBNAIL_IMAGE   — URL of the thumbnail image shown in the embed
    DISCORD_FOOTER_IMAGE      — URL of the small icon shown in the embed footer
"""
import logging
import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

# Discord embed colour — VASTIK brand purple
EMBED_COLOR = 0x7C3AED

# Timeout for the outbound webhook POST (seconds)
WEBHOOK_TIMEOUT = 8

# Topic → emoji mapping for a friendlier title
TOPIC_EMOJI = {
    "Commission Work":        "🎨",
    "Product Related Issue":  "📦",
    "Complaints":             "⚠️",
    "Suggestions":            "💡",
    "Others":                 "💬",
}


def send_discord_notification(sl_name: str, topic: str, message: str) -> bool:
    """
    Post a Discord embed notification for a newly submitted contact message.

    Args:
        sl_name:  The sender's Second Life username.
        topic:    The message topic (one of the SubmitContactSerializer choices).
        message:  The full message body.

    Returns:
        True on success, False on any failure (non-blocking — never raises).
    """
    webhook_url = getattr(settings, "DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        logger.warning(
            "[Discord] DISCORD_WEBHOOK_URL is not configured — skipping notification."
        )
        return False

    thumbnail_url = getattr(settings, "DISCORD_THUMBNAIL_IMAGE", "").strip()
    footer_image  = getattr(settings, "DISCORD_FOOTER_IMAGE",  "").strip()

    # ── Timestamp ──────────────────────────────────────────────────────────
    now        = timezone.now()
    # Discord accepts ISO-8601; it renders in the viewer's local timezone
    iso_ts     = now.isoformat()

    # Human-readable timestamp for the field (e.g. "April 28, 2026, 10:57 a.m.")
    readable_ts = now.strftime("%-d %B %Y, %-I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.")

    # ── Topic line ─────────────────────────────────────────────────────────
    emoji       = TOPIC_EMOJI.get(topic, "💬")
    embed_title = f"{emoji}  {topic}"

    # ── Build the embed ────────────────────────────────────────────────────
    embed = {
        "title":       embed_title,
        "description": (
            f"**Sender**\n"
            f"> `{sl_name}`\n\n"
            f"**Message**\n"
            f">>> {message}"
        ),
        "color": EMBED_COLOR,
        "timestamp": iso_ts,
        "fields": [
            {
                "name":   "Verified",
                "value":  "✅  OTP Verified",
                "inline": True,
            },
            {
                "name":   "Received",
                "value":  readable_ts,
                "inline": True,
            },
        ],
        "footer": {
            "text":     "Vastik Messenger  •  via VASTIK Website",
            "icon_url": footer_image if footer_image else None,
        },
    }

    # Remove None values Discord would reject
    if not embed["footer"]["icon_url"]:
        del embed["footer"]["icon_url"]

    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}

    # ── Webhook payload ────────────────────────────────────────────────────
    payload = {
        # The "app name" shown above the embed card
        "username":   "VASTIK Messenger",
        "embeds":     [embed],
    }

    # ── POST to Discord ────────────────────────────────────────────────────
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=WEBHOOK_TIMEOUT,
        )

        # Discord returns 204 No Content on success
        if response.status_code in (200, 204):
            logger.info(
                f"[Discord] Notification sent for message from '{sl_name}' (topic: {topic})"
            )
            return True
        else:
            logger.error(
                f"[Discord] Webhook returned HTTP {response.status_code}: {response.text[:200]}"
            )
            return False

    except requests.exceptions.Timeout:
        logger.error("[Discord] Webhook request timed out.")
        return False
    except requests.exceptions.ConnectionError as exc:
        logger.error(f"[Discord] Connection error posting to webhook: {exc}")
        return False
    except Exception as exc:
        logger.error(f"[Discord] Unexpected error: {exc}")
        return False
