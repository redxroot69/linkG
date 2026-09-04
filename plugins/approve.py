# +++ Modified By Yato [telegram username: @i_killed_my_clan & @Feudalmaster] +++ # aNDI BANDI SANDI JISNE BHI CREDIT HATAYA USKI BANDI RAndi 
import os
import asyncio
import time
from typing import List
from config import *
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import Message, User, ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, ChatAdminRequired, RPCError, UserNotParticipant, UserAlreadyParticipant
from database.database import set_approval_off, is_approval_off, get_channels, get_channel_settings, set_channel_approval, set_channel_wait_time, save_encoded_link, save_encoded_link2
from helper_func import *

async def get_user_client():
    global user_client
    if user_client is None:
        user_client = UserClient("userbot", session_string=USER_SESSION, api_id=APP_ID, api_hash=API_HASH)
        await user_client.start()
    return user_client


async def _send_request_welcome(client, chat, user):
    """Best-effort welcome DM sent when a user requests to join a chat.
    Fails silently for users who never started the bot or blocked it."""
    try:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton('• ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs •', url='https://t.me/MalluHaven')],
        ])
        caption = (
            f"<b>ʜᴇʏ {user.mention()},</b>\n\n"
            f"<blockquote>ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ <b>{chat.title}</b> ʜᴀs ʙᴇᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ ✅\n"
            f"ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ, ɪᴛ ᴡɪʟʟ ʙᴇ ᴀᴘᴘʀᴏᴠᴇᴅ sʜᴏʀᴛʟʏ.</blockquote>"
        )
        await client.send_photo(
            chat_id=user.id,
            photo='https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg',
            caption=caption,
            reply_markup=buttons
        )
        print(f"Request welcome sent to {user.id} for {chat.id}")
    except Exception as e:
        print(f"Could not send request welcome to {user.id} for {chat.id}: {e}")


@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user

    settings = await get_channel_settings(chat.id)

    # check agr approval of hai us chnl m
    if not settings["approval_enabled"]:
        print(f"Auto-approval is OFF for channel {chat.id}")
        return

    print(f"{user.first_name} requested to join {chat.title}")

    await _send_request_welcome(client, chat, user)

    await asyncio.sleep(settings["approval_wait_time"])

    # Check if user is already a participant before approving
    try:
        member = await client.get_chat_member(chat.id, user.id)
        if member.status in ["member", "administrator", "creator"]:
            print(f"User {user.id} is already a participant of {chat.id}, skipping approval.")
            return
    except UserNotParticipant:
        # User is not a member, handle accordingly
        pass

    try:
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    except UserAlreadyParticipant:
        print(f"User {user.id} is already a participant of {chat.id}, skipping approval.")
        return
    except Exception as e:
        print(f"Failed to approve {user.id} for {chat.id}: {e}")
        return

    if APPROVED == "on":
        invite_link = await client.export_chat_invite_link(chat.id)
        buttons = [
            [InlineKeyboardButton('• ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs •', url='https://t.me/MalluHaven')],
            [InlineKeyboardButton(f'• ᴊᴏɪɴ {chat.title} •', url=invite_link)]
        ]
        markup = InlineKeyboardMarkup(buttons)
        caption = f"<b>ʜᴇʏ {user.mention()},\n\n<blockquote> ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ _{chat.title} ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ.</blockquote> </b>"

        try:
            await client.send_photo(
                chat_id=user.id,
                photo='https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg',
                caption=caption,
                reply_markup=markup
            )
        except Exception as e:
            print(f"Could not send approval message to {user.id} for {chat.id}: {e}")


async def can_manage_chat(client, user_id, channel_id: int, message=None) -> bool:
    """Allow if the user registered the chat via /addch OR is a Telegram admin of it.

    Anonymous admins (user_id None) are allowed only when the command was posted
    anonymously from inside that very chat: Telegram hides their identity, but only
    a real admin of a chat can send as that chat, so sender_chat == channel_id is
    enough proof.
    """
    if user_id is not None:
        if channel_id in await get_channels(user_id):
            return True
        try:
            member = await client.get_chat_member(channel_id, user_id)
            return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
        except Exception:
            return False
    # Anonymous admin / chat post: prove the sender acts on behalf of this chat.
    # The chat can be exposed either as message.sender_chat or, when the sender is
    # only known as the special anonymous user, as message.chat (the chat the
    # command was typed in). Only a real admin can send as the chat, so matching
    # the target channel is enough proof.
    if message is not None:
        sender_chat = getattr(message, "sender_chat", None)
        acted_chat = sender_chat.id if sender_chat is not None else getattr(message, "chat", None) and message.chat.id
        if acted_chat == channel_id:
            print(f"Anonymous admin of {channel_id} granted management access (acted on behalf of the chat)")
            return True
    return False


async def resolve_target_chat(client, message, channel_id_str, usage):
    """Return the target channel id, or None after sending a usage/error message."""
    if channel_id_str:
        try:
            return int(channel_id_str)
        except ValueError:
            await message.reply_text("❌ Invalid channel ID.")
            return None
    if message.chat.type == ChatType.PRIVATE:
        await message.reply_text(usage)
        return None
    return message.chat.id


# ---------------------------------------------------------------------------
# /settings -> connected-chat list -> per-chat management menu
# ---------------------------------------------------------------------------
SETTINGS_LIST_PAGE_SIZE = 6
TIME_INPUT_TIMEOUT = 90

# Per-user conversational state while the bot asks for the approval timer
waiting_time_input = {}  # key -> {"chat_id": int, "channel_id": int, "expires": float}


def _waiting_key(message) -> tuple:
    """Identity key for the waiting state: the real user id, or the chat itself
    when the sender is an (anonymous) admin acting on behalf of the chat."""
    uid = sender_user_id(message)
    if uid is not None:
        return ("user", uid)
    src = message.message if getattr(message, "message", None) is not None else message
    chat_id = None
    sender_chat = getattr(src, "sender_chat", None)
    if sender_chat is not None:
        chat_id = sender_chat.id
    elif getattr(src, "chat", None) is not None:
        chat_id = src.chat.id
    return ("chat", chat_id)


def _clear_waiting(message) -> bool:
    return waiting_time_input.pop(_waiting_key(message), None) is not None


def _who(source) -> str:
    """Short identity for log lines: real user id, or the chat for anonymous admins."""
    uid = sender_user_id(source)
    if uid is not None:
        return str(uid)
    return f"anon(chat {_waiting_key(source)[1]})"


async def _chat_title(client, channel_id: int) -> str:
    try:
        chat = await client.get_chat(channel_id)
        return chat.title or str(channel_id)
    except Exception:
        return str(channel_id)


async def _connected_settings_chats(client, source) -> List[int]:
    """Chats shown in the /settings list: chats the sender registered via /addch,
    plus the chat the command was typed in when the sender can manage it."""
    uid = sender_user_id(source)
    chats = []
    if uid is not None:
        chats = list(await get_channels(uid))
    src_chat = getattr(source, "chat", None)
    if src_chat is None and getattr(source, "message", None) is not None:
        src_chat = getattr(source.message, "chat", None)
    if src_chat is not None and src_chat.type != ChatType.PRIVATE and src_chat.id not in chats:
        ctx = source.message if getattr(source, "message", None) is not None else source
        if await can_manage_chat(client, uid, src_chat.id, message=ctx):
            chats.insert(0, src_chat.id)
    seen, out = set(), []
    for c in chats:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


async def _render_settings_list(client, target, chats, page=0, edit=False):
    total_pages = max(1, (len(chats) + SETTINGS_LIST_PAGE_SIZE - 1) // SETTINGS_LIST_PAGE_SIZE)
    page = min(max(page, 0), total_pages - 1)
    buttons = []
    for cid in chats[page * SETTINGS_LIST_PAGE_SIZE:(page + 1) * SETTINGS_LIST_PAGE_SIZE]:
        buttons.append([InlineKeyboardButton(await _chat_title(client, cid), callback_data=f"sch_{cid}")])
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("‹ Pʀᴇᴠ", callback_data=f"schp_{page - 1}"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton("Nᴇxᴛ ›", callback_data=f"schp_{page + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton("• Close •", callback_data="close")])
    text = (
        "<b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\n"
        "<blockquote expandable>Select a chat below to manage it:\n"
        "🔗 Nᴏʀᴍᴀʟ Lɪɴᴋ – get its shareable join link\n"
        "🔗 Rᴇǫᴜᴇsᴛ Lɪɴᴋ – get its join-request link\n"
        "⏱️ Rᴇǫᴜᴇsᴛ Tɪᴍᴇ – set the approval timer (seconds)\n"
        "🤖 Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴀʟ – turn auto-approve on/off</blockquote>"
    )
    if chats:
        text += f"\n\n<b>Cᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀᴛs ({len(chats)}):</b>"
    markup = InlineKeyboardMarkup(buttons)
    if edit:
        try:
            await target.edit_text(text, reply_markup=markup)
        except Exception:
            await target.reply(text, reply_markup=markup)
    else:
        await target.reply(text, reply_markup=markup)


async def _render_chat_menu(client, query, channel_id):
    settings = await get_channel_settings(channel_id)
    title = await _chat_title(client, channel_id)
    status = "🟢 ᴏɴ" if settings["approval_enabled"] else "🔴 ᴏғғ"
    text = (
        f"<b>⚙️ {title}</b>\n\n"
        f"<blockquote>🤖 Aᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇ: {status}\n"
        f"⏱️ Rᴇǫᴜᴇsᴛ ᴛɪᴍᴇ: {settings['approval_wait_time']} sᴇᴄᴏɴᴅs</blockquote>\n\n"
        f"<i>Wʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏ?</i>"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Nᴏʀᴍᴀʟ Lɪɴᴋ", callback_data=f"snorm_{channel_id}"),
         InlineKeyboardButton("🔗 Rᴇǫᴜᴇsᴛ Lɪɴᴋ", callback_data=f"sreq_{channel_id}")],
        [InlineKeyboardButton("⏱️ Rᴇǫᴜᴇsᴛ Tɪᴍᴇ", callback_data=f"stime_{channel_id}")],
        [InlineKeyboardButton("🤖 Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴀʟ", callback_data=f"saa_{channel_id}")],
        [InlineKeyboardButton("‹ Bᴀᴄᴋ Tᴏ Cʜᴀᴛ Lɪsᴛ", callback_data="sch_back")]
    ])
    try:
        await query.message.edit_text(text, reply_markup=buttons)
    except Exception:
        await query.message.reply(text, reply_markup=buttons)


async def _render_aa_menu(client, query, channel_id):
    settings = await get_channel_settings(channel_id)
    title = await _chat_title(client, channel_id)
    status = "🟢 Oɴ" if settings["approval_enabled"] else "🔴 Oғғ"
    text = (f"<b>🤖 Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴀʟ — {title}</b>\n\n"
            f"<blockquote>Cᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs: {status}</blockquote>\n\n"
            f"<i>Sᴇʟᴇᴄᴛ Oɴ ᴏʀ Oғғ:</i>")
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Oɴ", callback_data=f"saa_on_{channel_id}"),
         InlineKeyboardButton("❌ Oғғ", callback_data=f"saa_off_{channel_id}")],
        [InlineKeyboardButton("‹ Bᴀᴄᴋ", callback_data=f"sch_{channel_id}")]
    ])
    await query.message.edit_text(text, reply_markup=buttons)


async def _render_time_prompt(client, query, channel_id):
    title = await _chat_title(client, channel_id)
    waiting_time_input[_waiting_key(query)] = {
        "chat_id": query.message.chat.id,
        "channel_id": channel_id,
        "expires": time.time() + TIME_INPUT_TIMEOUT,
    }
    text = (
        f"<b>⏱️ Rᴇǫᴜᴇsᴛ Tɪᴍᴇ — {title}</b>\n\n"
        f"<blockquote>sᴇᴛ ᴀᴘᴘʀᴏᴠᴀʟ ᴛɪᴍᴇʀ ɪɴ sᴇᴄᴏɴᴅs.\n"
        f"Rᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ sᴇᴄᴏɴᴅs (ᴇ.ɢ. <code>5</code>).</blockquote>"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("‹ Bᴀᴄᴋ", callback_data=f"sch_{channel_id}")]
    ])
    await query.message.edit_text(text, reply_markup=buttons)


async def _build_share_links(client, channel_id):
    normal_enc = await save_encoded_link(channel_id)
    normal = f"https://t.me/{client.username}?start={normal_enc}"
    req_enc = await encode(str(channel_id))
    await save_encoded_link2(channel_id, req_enc)
    request = f"https://t.me/{client.username}?start=req_{req_enc}"
    return normal, request


@Client.on_message(filters.command("settings"))
async def settings_command(client, message: Message):
    args = message.command
    usage = "Usage: <code>/settings [channel_id]</code> (in a group) or <code>/settings &lt;channel_id&gt;</code> (in DM)"

    # /settings time <seconds> [channel_id]
    if len(args) > 1 and args[1].lower() == "time":
        if len(args) not in (3, 4) or not args[2].isdigit():
            return await message.reply_text("Usage: <code>/settings time &lt;seconds&gt; [channel_id]</code>")
        seconds = int(args[2])
        channel_id = await resolve_target_chat(client, message, args[3] if len(args) == 4 else None,
                                               "Usage in DM: <code>/settings time &lt;seconds&gt; &lt;channel_id&gt;</code>")
        if channel_id is None:
            return
        if not await can_manage_chat(client, sender_user_id(message), channel_id, message=message):
            return await message.reply_text("❌ Only chat admins or the registered owner can change this.\n<i>Tip: anonymous admins can manage a chat by sending the command inside that chat.</i>")
        await set_channel_wait_time(channel_id, seconds)
        return await message.reply_text(f"✅ Wait time set to <b>{seconds}</b> seconds for this chat.")

    chats = await _connected_settings_chats(client, message)
    print(f"SETTINGS: {_who(message)} opened settings menu ({len(chats)} chats)")
    if not chats:
        return await message.reply_text(
            "<b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\n"
            "<blockquote>Nᴏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀᴛs ʏᴇᴛ.</blockquote>\n\n"
            "ᴀᴅᴅ ᴀ ᴄʜᴀᴛ ᴡɪᴛʜ <code>/addch &lt;chat_id&gt;</code>, ᴏʀ sᴇɴᴅ <code>/settings</code> ɪɴsɪᴅᴇ ᴀ ɢʀᴏᴜᴘ ʏᴏᴜ ᴀᴅᴍɪɴ ᴛᴏ ᴍᴀɴᴀɢᴇ ɪᴛ."
        )
    await _render_settings_list(client, message, chats)


@Client.on_callback_query(filters.regex(r"^schp_(\d+)$"))
async def settings_list_page(client, callback_query):
    page = int(callback_query.data.split("_", 1)[1])
    chats = await _connected_settings_chats(client, callback_query)
    if not chats:
        return await callback_query.answer("No connected chats", show_alert=True)
    await _render_settings_list(client, callback_query.message, chats, page=page, edit=True)
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"^sch_(-?\d+)$"))
async def settings_open_chat(client, callback_query):
    channel_id = int(callback_query.data.split("_", 1)[1])
    _clear_waiting(callback_query)
    if not await can_manage_chat(client, callback_user_id(callback_query), channel_id, message=callback_query.message):
        print(f"SETTINGS: {_who(callback_query)} DENIED for chat {channel_id}")
        return await callback_query.answer("Not allowed", show_alert=True)
    print(f"SETTINGS: {_who(callback_query)} opened chat {channel_id}")
    await _render_chat_menu(client, callback_query, channel_id)
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"^sch_back$"))
async def settings_back_to_list(client, callback_query):
    _clear_waiting(callback_query)
    chats = await _connected_settings_chats(client, callback_query)
    if not chats:
        await callback_query.message.edit_text("<b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nNᴏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀᴛs.")
        return await callback_query.answer()
    await _render_settings_list(client, callback_query.message, chats, edit=True)
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"^(snorm|sreq)_(-?\d+)$"))
async def settings_link_button(client, callback_query):
    kind, channel_id = callback_query.data.split("_", 1)
    channel_id = int(channel_id)
    if not await can_manage_chat(client, callback_user_id(callback_query), channel_id, message=callback_query.message):
        print(f"SETTINGS: {_who(callback_query)} DENIED {kind} for chat {channel_id}")
        return await callback_query.answer("Not allowed", show_alert=True)
    print(f"SETTINGS: {_who(callback_query)} requested {kind} link of chat {channel_id}")
    try:
        normal, request = await _build_share_links(client, channel_id)
    except Exception as e:
        print(f"Failed to build share links for {channel_id}: {e}")
        return await callback_query.answer("Could not build the link", show_alert=True)
    title = await _chat_title(client, channel_id)
    if kind == "snorm":
        text = (f"<b>🔗 Nᴏʀᴍᴀʟ Lɪɴᴋ — {title}</b>\n\n"
                f"<code>{normal}</code>\n\n<i>Users open this to get a join link for the chat.</i>")
    else:
        text = (f"<b>🔗 Rᴇǫᴜᴇsᴛ Lɪɴᴋ — {title}</b>\n\n"
                f"<code>{request}</code>\n\n<i>Users must be approved before they can join.</i>")
    await callback_query.message.reply(text)
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"^stime_(-?\d+)$"))
async def settings_time_prompt(client, callback_query):
    channel_id = int(callback_query.data.split("_", 1)[1])
    if not await can_manage_chat(client, callback_user_id(callback_query), channel_id, message=callback_query.message):
        return await callback_query.answer("Not allowed", show_alert=True)
    print(f"SETTINGS: {_who(callback_query)} asked to set request time for chat {channel_id}")
    await _render_time_prompt(client, callback_query, channel_id)
    await callback_query.answer()


@Client.on_message(filters.text)
async def settings_time_answer(client, message: Message):
    pending = waiting_time_input.get(_waiting_key(message))
    if not pending:
        return
    if pending["chat_id"] != message.chat.id:
        return
    if time.time() > pending.get("expires", 0):
        waiting_time_input.pop(_waiting_key(message), None)
        return
    value = message.text.strip()
    if not value.isdigit():
        if value.startswith("/"):
            return  # let commands through, keep waiting
        return await message.reply_text("⏱️ ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ᴛɪᴍᴇ ᴀs ᴀ ɴᴜᴍʙᴇʀ ɪɴ sᴇᴄᴏɴᴅs, ᴏʀ ᴘʀᴇss ‹ Bᴀᴄᴋ.")
    key = _waiting_key(message)
    waiting_time_input.pop(key, None)
    channel_id = pending["channel_id"]
    if not await can_manage_chat(client, sender_user_id(message), channel_id, message=message):
        return await message.reply_text("❌ Only chat admins or the registered owner can change this.")
    seconds = int(value)
    await set_channel_wait_time(channel_id, seconds)
    print(f"SETTINGS: {_who(message)} set request time of chat {channel_id} to {seconds}s")
    await message.reply_text(f"✅ Rᴇǫᴜᴇsᴛ ᴛɪᴍᴇ sᴇᴛ ᴛᴏ <b>{seconds}</b> sᴇᴄᴏɴᴅs.")


@Client.on_callback_query(filters.regex(r"^saa_(-?\d+)$"))
async def settings_aa_menu(client, callback_query):
    channel_id = int(callback_query.data.split("_", 1)[1])
    if not await can_manage_chat(client, callback_user_id(callback_query), channel_id, message=callback_query.message):
        return await callback_query.answer("Not allowed", show_alert=True)
    await _render_aa_menu(client, callback_query, channel_id)
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"^saa_(on|off)_(-?\d+)$"))
async def settings_aa_toggle(client, callback_query):
    action = callback_query.data.split("_")[1]
    channel_id = int(callback_query.data.split("_")[2])
    if not await can_manage_chat(client, callback_user_id(callback_query), channel_id, message=callback_query.message):
        return await callback_query.answer("Not allowed", show_alert=True)
    await set_channel_approval(channel_id, action == "on")
    print(f"SETTINGS: {_who(callback_query)} turned auto-approval {'ON' if action == 'on' else 'OFF'} for chat {channel_id}")
    await _render_aa_menu(client, callback_query, channel_id)
    await callback_query.answer(f"Auto-approval turned {'ON' if action == 'on' else 'OFF'}")


# ---- Per-chat aliases (old commands keep working) ----

@Client.on_message(filters.command("reqtime"))
async def set_reqtime(client, message: Message):
    args = message.command
    if len(args) not in (2, 3) or not args[1].isdigit():
        return await message.reply_text("Usage: <code>/reqtime {seconds} [channel_id]</code>")
    channel_id = await resolve_target_chat(client, message, args[2] if len(args) == 3 else None,
                                           "Usage in DM: <code>/reqtime &lt;seconds&gt; &lt;channel_id&gt;</code>")
    if channel_id is None:
        return
    if not await can_manage_chat(client, sender_user_id(message), channel_id, message=message):
        return await message.reply_text("❌ Only chat admins or the registered owner can change this.\n<i>Tip: anonymous admins can manage a chat by sending the command inside that chat.</i>")
    await set_channel_wait_time(channel_id, int(args[1]))
    await message.reply_text(f"✅ Wait time set to <b>{args[1]}</b> seconds for this chat.")


@Client.on_message(filters.command("reqmode"))
async def toggle_reqmode(client, message: Message):
    args = message.command
    if len(args) not in (2, 3) or args[1].lower() not in ["on", "off"]:
        return await message.reply_text("Usage: <code>/reqmode on|off [channel_id]</code>")
    channel_id = await resolve_target_chat(client, message, args[2] if len(args) == 3 else None,
                                           "Usage in DM: <code>/reqmode on|off &lt;channel_id&gt;</code>")
    if channel_id is None:
        return
    if not await can_manage_chat(client, sender_user_id(message), channel_id, message=message):
        return await message.reply_text("❌ Only chat admins or the registered owner can change this.\n<i>Tip: anonymous admins can manage a chat by sending the command inside that chat.</i>")
    mode = args[1].lower()
    await set_channel_approval(channel_id, mode == "on")
    status = "enabled ✅" if mode == "on" else "disabled ❌"
    await message.reply_text(f"Auto-approval for this chat has been {status}.")


@Client.on_message(filters.command("approveoff"))
async def approve_off_command(client, message: Message):
    if len(message.command) != 2 or not message.command[1].lstrip("-").isdigit():
        return await message.reply_text("Usage: <code>/approveoff {channel_id}</code>")
    channel_id = int(message.command[1])
    if not await can_manage_chat(client, sender_user_id(message), channel_id, message=message):
        return await message.reply_text("❌ Channel not in your list. Add it first with /addch.\n<i>Tip: anonymous admins can manage a chat by sending the command inside that chat.</i>")
    success = await set_approval_off(channel_id, True)
    if success:
        await message.reply_text(f"✅ Auto-approval is now <b>OFF</b> for channel <code>{channel_id}</code>.")
    else:
        await message.reply_text(f"❌ Failed to set auto-approval OFF for channel <code>{channel_id}</code>.")


@Client.on_message(filters.command("approveon"))
async def approve_on_command(client, message: Message):
    if len(message.command) != 2 or not message.command[1].lstrip("-").isdigit():
        return await message.reply_text("Usage: <code>/approveon {channel_id}</code>")
    channel_id = int(message.command[1])
    if not await can_manage_chat(client, sender_user_id(message), channel_id, message=message):
        return await message.reply_text("❌ Channel not in your list. Add it first with /addch.\n<i>Tip: anonymous admins can manage a chat by sending the command inside that chat.</i>")
    success = await set_approval_off(channel_id, False)
    if success:
        await message.reply_text(f"✅ Auto-approval is now <b>ON</b> for channel <code>{channel_id}</code>.")
    else:
        await message.reply_text(f"❌ Failed to set auto-approval ON for channel <code>{channel_id}</code>.")