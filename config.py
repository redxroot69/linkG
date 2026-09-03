# +++ Modified By [telegram username: @Codeflix_Bots
import os
from os import environ
import logging
from logging.handlers import RotatingFileHandler

# Recommended
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

# Main
OWNER_ID = int(os.environ.get("OWNER_ID", "6497757690"))
PORT = os.environ.get("PORT", "8080")

# Database
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "link")

#Auto approve 
CHAT_ID = [int(app_chat_id) if id_pattern.search(app_chat_id) else app_chat_id for app_chat_id in environ.get('CHAT_ID', '').split()] # dont change anything 
TEXT = environ.get("APPROVED_WELCOME_TEXT", "<b>{mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n\‣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Codeflix_Bots</b>")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

# Default
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "40"))
#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -

# Start pic
START_PIC = "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg"
START_IMG = "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg"
# Messages
START_MSG = os.environ.get("START_MESSAGE", "<b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ʟɪɴᴋs sʜᴀʀɪɴɢ ʙᴏᴛ. ᴡɪᴛʜ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴄᴀɴ sʜᴀʀᴇ ʟɪɴᴋs ᴀɴᴅ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs sᴀғᴇ ғʀᴏᴍ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.\n\n<blockquote>‣ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/codeflix_bots'>ʏᴀᴛᴏ</a></blockquote></b>")
HELP = os.environ.get("HELP_MESSAGE", """<b>ʜᴇʟᴘ / ᴄᴏᴍᴍᴀɴᴅs:</b>

<blockquote><b>👤 Usᴇʀ</b>
/start — sᴛᴀʀᴛ ʙᴏᴛ / ᴏᴘᴇɴ sʜᴀʀᴇᴅ ʟɪɴᴋs

<b>📢 Cʜᴀɴɴᴇʟ & Lɪɴᴋs (Aᴅᴍɪɴ)</b>
/addch <id> — ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ
/delch <id> — ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ
/channels — sʜᴏᴡ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀɴɴᴇʟs (ɪᴅ & ɴᴀᴍᴇ)
/ch_links — sʜᴏᴡ ᴄʜᴀɴɴᴇʟs ᴀs ʙᴜᴛᴛᴏɴs
/links — sʜᴏᴡ ᴄʜᴀɴɴᴇʟ ʟɪɴᴋs
/reqlink — sʜᴏᴡ ʀᴇǫᴜᴇsᴛ ʟɪɴᴋs
/bulklink <id1> <id2>… — ʙᴜʟᴋ ʟɪɴᴋs
/genlink <link> — ᴍᴀᴋᴇ ᴀ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ

<b>✅ Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴇ (ᴘᴇʀ ᴄʜᴀᴛ)</b>
/settings [id] — ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs ᴠɪᴀ ʙᴜᴛᴛᴏɴs
/settings time <sec> [id] — ᴄᴜsᴛᴏᴍ ᴡᴀɪᴛ ᴛɪᴍᴇ
/reqtime <sec> [id] — sᴇᴛ ᴀᴘᴘʀᴏᴠᴀʟ ᴛɪᴍᴇʀ
/reqmode on|off [id] — ᴛᴏɢɢʟᴇ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴀʟ
/approveon <id> — ᴏɴ ғᴏʀ ᴄʜᴀɴɴᴇʟ
/approveoff <id> — ᴏғғ ғᴏʀ ᴄʜᴀɴɴᴇʟ

<b>📣 Bʀᴏᴀᴅᴄᴀsᴛ (Aᴅᴍɪɴ)</b>
/broadcast [pin] [delete N] [silent] — ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ
/cancel — sᴛᴏᴘ ʙʀᴏᴀᴅᴄᴀsᴛ
/status — ʙᴏᴛ sᴛᴀᴛᴜs

<b>⚙️ Oᴡɴᴇʀ Oɴʟʏ</b>
/stats — ᴜᴘᴛɪᴍᴇ sᴛᴀᴛs
/addadmin <id> — ᴀᴅᴅ ᴀᴅᴍɪɴ
/deladmin <id> — ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ
/admins — ʟɪsᴛ ᴀᴅᴍɪɴs</blockquote>""")
ABOUT = os.environ.get("ABOUT_MESSAGE", "<b><blockquote expandable>This bot is developed by Yato (@ProYato) to securely share Telegram channel links with temporary invite links, protecting your channels from copyright issues.</b>")

ABOUT_TXT = """<b>›› ᴄᴏᴍᴍᴜɴɪᴛʏ: <a href='https://t.me/otakuflix_network'>ᴏᴛᴀᴋᴜғʟɪx</a>
<blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/codeflix_bots'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>
›› ᴏᴡɴᴇʀ: <a href='https://t.me/cosmic_freak'>ʏᴀᴛᴏ</a>
›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>
›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>
›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a>
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ProYato</b></blockquote>""" # Bhosdiwalo agar developer me Yato ka username hataya to agli baar se koi repo public nhi krunga!!

CHANNELS_TXT = """<b>›› ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/animes_cruise'>ᴀɴɪᴍᴇ ᴄʀᴜɪsᴇ</a>
<blockquote expandable>›› ᴍᴏᴠɪᴇs: <a href='https://t.me/movieflixspot'>ᴍᴏᴠɪᴇғʟɪx sᴘᴏᴛ</a>
›› ᴡᴇʙsᴇʀɪᴇs: <a href='https://t.me/webseries_flix'>ᴡᴇʙsᴇʀɪᴇs ғʟɪx</a>
›› ᴀᴅᴜʟᴛ ᴄʜᴀɴɴᴇʟs: <a href='https://t.me/hanime_arena'>ᴄᴏʀɴʜᴜʙ</a>
›› ᴍᴀɴʜᴡᴀ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/pornhwa_flix'>ᴘᴏʀɴʜᴡᴀ</a>
›› ᴄᴏᴍᴍᴜɴɪᴛʏ: <a href='https://t.me/otakuflix_network'>ᴏᴛᴀᴋᴜғʟɪx</a>
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ProYato</b></blockquote>""" # Bhosdiwalo agar developer me Yato ka username hataya to agli baar se koi repo public nhi krunga!!

#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -
# Default
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "⚠️ ғᴜᴄᴋ ʏᴏᴜ, ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃!"

# Logging
LOG_FILE_NAME = "links-sharingbot.txt"
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", "")) # Channel where user links are stored
#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -

try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "6497757690").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Admin == OWNER_ID
ADMINS.append(OWNER_ID)
ADMINS.append(6497757690)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
