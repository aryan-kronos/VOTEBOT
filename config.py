# ==============================================================================
# 🚀 ADVANCED TELEGRAM GIVEAWAY & VOTING BOT ENGINE
# 👨‍💻 DEVELOPED & BUILT BY: ARYAN (@thatonearyan)
# 🔗 TELEGRAM CONTACT: https://t.me/thatonearyan
# 🌐 OFFICIAL DEVELOPER CHANNEL: https://t.me/thatonearyan
# 💎 CORE ARCHITECTURE & LOGIC CRAFTED BY ARYAN (@thatonearyan)
# ⚡ COPYRIGHT (C) ARYAN - ALL RIGHTS RESERVED - https://t.me/thatonearyan
# ==============================================================================

import os
from dotenv import load_dotenv
from aiogram.enums import ParseMode

load_dotenv()

# Bot Credentials
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "YourVoteBot")  # without @

# Database
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Votebot")

# Administrators
ADMINS = [int(x.strip()) for x in os.getenv("ADMINS", "").split(",") if x.strip()]

# Logging Channels
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0")) if os.getenv("LOG_CHANNEL_ID") else None
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
LOG_GROUP_ID = os.getenv("LOG_GROUP_ID", "")

# Brand Names & Titles
BOT_NAME = os.getenv("BOT_NAME", "BITZ GIVEAWAY BOT")
BOT_NAME_STYLED = os.getenv("BOT_NAME_STYLED", "𝐁𝐈𝐓𝐙 𝐆𝐈𝐕𝐄𝐀𝐖𝐀𝐘 𝐁𝐎𝐓!")
BRAND_NAME = os.getenv("BRAND_NAME", "BITZ")
BRAND_NAME_SMALLCAPS = os.getenv("BRAND_NAME_SMALLCAPS", "ʙɪᴛᴢ")

# Network / Channel
NETWORK_NAME = os.getenv("NETWORK_NAME", "ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ")
NETWORK_USERNAME = os.getenv("NETWORK_USERNAME", "tgbitz")
NETWORK_URL = os.getenv("NETWORK_URL", f"https://t.me/{NETWORK_USERNAME}")

# Support & Admin
SUPPORT_NAME = os.getenv("SUPPORT_NAME", "ᴅᴇᴠᴀɴꜱʜ")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "tgbitz_op")
SUPPORT_URL = os.getenv("SUPPORT_URL", f"https://t.me/{SUPPORT_USERNAME}")

# Permanent Developer Attribution (Hardcoded)
DEVELOPER_NAME = "ᴀʀʏᴀɴ"
DEVELOPER_USERNAME = "thatonearyan"
DEVELOPER_URL = "https://t.me/thatonearyan"

# Guides & Media
HOW_TO_USE_URL = os.getenv("HOW_TO_USE_URL", NETWORK_URL)
START_IMAGE = os.getenv("START_IMAGE", "https://files.catbox.moe/kd21dg.jpg")
PARTICIPANT_IMAGE = os.getenv("PARTICIPANT_IMAGE", "https://files.catbox.moe/xj0ci0.jpg")
VOTE_IMAGE_URL = os.getenv("VOTE_IMAGE_URL", "https://files.catbox.moe/mkfcpr.jpg")
DEFAULT_UPI_ID = os.getenv("DEFAULT_UPI_ID", "devanshsingh2@fam")
DEFAULT_PLANS = os.getenv("DEFAULT_PLANS", "7D 49 15D 89 30D 149")

# Parse Mode
PARSE_MODE = ParseMode.HTML
