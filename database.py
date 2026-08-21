# ==============================================================================
# 🚀 ADVANCED TELEGRAM GIVEAWAY & VOTING BOT ENGINE
# 👨‍💻 DEVELOPED & BUILT BY: ARYAN (@thatonearyan)
# 🔗 TELEGRAM CONTACT: https://t.me/thatonearyan
# 🌐 OFFICIAL DEVELOPER CHANNEL: https://t.me/thatonearyan
# 💎 CORE ARCHITECTURE & LOGIC CRAFTED BY ARYAN (@thatonearyan)
# ⚡ COPYRIGHT (C) ARYAN - ALL RIGHTS RESERVED - https://t.me/thatonearyan
# ==============================================================================

import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# CONFIGURATION
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Votebot")

# Initialize Client
client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DATABASE_NAME]

# Collections
giveaways_col = db['giveaways']
votes_col = db['votes']
participants_col = db['participants']
users_col = db['users']

# System & Settings Collections
transactions_col = db['transactions']     # Stores pending paid vote/membership requests
memberships_col = db['memberships']       # Stores active force-join channels
membership_settings_col = db['membership_settings'] # Stores prices, plans, UPI
settings_col = db['settings']             # Stores admin settings and templates
start_settings_col = db['start_settings'] # Stores custom welcome messages
channels_col = db['channels']             # Stores channels where bot is admin
