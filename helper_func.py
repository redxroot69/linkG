# +++ Modified By Yato [telegram username: @i_killed_my_clan & @Feudalmaster] +++ # aNDI BANDI SANDI JISNE BHI CREDIT HATAYA USKI BANDI RAndi 
import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import ADMINS
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.filters import Filter
from config import OWNER_ID
from database.database import is_admin

# Telegram hides the identity of "anonymous admins" in groups. Pyrogram receives
# their messages with from_user=None and sender_chat=<the chat>; the id below is
# only what Bot-API-style clients see for the same sender.
ANONYMOUS_ADMIN_ID = 1087968824


def resolve_sender(message):
    """Return (user_id, sender_chat_id) for a Message or CallbackQuery.

    - Regular user -> (their id, None)
    - Anonymous admin in a group -> (None, the group id). Telegram hides the real
      identity, but only a real admin of that chat can send as the anonymous admin.
    - Channel post -> (None, the channel id), for the same reason.
    """
    from_user = getattr(message, "from_user", None)
    if from_user is not None:
        uid = getattr(from_user, "id", None)
        if uid == ANONYMOUS_ADMIN_ID:
            return None, None
        return uid, None
    sender_chat = getattr(message, "sender_chat", None)
    if sender_chat is not None:
        return None, sender_chat.id
    return None, None


def sender_user_id(message):
    """Effective user id of the sender; None for anonymous admins / chat posts."""
    return resolve_sender(message)[0]


def callback_user_id(callback_query):
    """Effective user id of a callback query sender; None if hidden (anonymous)."""
    return sender_user_id(callback_query)


class IsAdmin(Filter):
    async def __call__(self, client, message):
        return await is_admin(message.from_user.id)

is_admin_filter = IsAdmin()

class IsOwnerOrAdmin(Filter):
    async def __call__(self, client, message):
        user_id = message.from_user.id
        return user_id == OWNER_ID or user_id in ADMINS or await is_admin(user_id)

is_owner_or_admin = IsOwnerOrAdmin()

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time
