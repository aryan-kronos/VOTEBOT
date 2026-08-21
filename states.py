# ==============================================================================
# 🚀 ADVANCED TELEGRAM GIVEAWAY & VOTING BOT ENGINE
# 👨‍💻 DEVELOPED & BUILT BY: ARYAN (@thatonearyan)
# 🔗 TELEGRAM CONTACT: https://t.me/thatonearyan
# 🌐 OFFICIAL DEVELOPER CHANNEL: https://t.me/thatonearyan
# 💎 CORE ARCHITECTURE & LOGIC CRAFTED BY ARYAN (@thatonearyan)
# ⚡ COPYRIGHT (C) ARYAN - ALL RIGHTS RESERVED - https://t.me/thatonearyan
# ==============================================================================

from aiogram.fsm.state import State, StatesGroup

# Giveaway Creation
# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class CreateGiveaway(StatesGroup):
    waiting_for_description = State()
    waiting_for_target_channel = State()
    waiting_for_force_channels = State()
    # New Paid Vote States
    waiting_for_paid_confirm = State()
    waiting_for_payment_methods = State()
    waiting_for_upi_qr = State()
    waiting_for_upi_id = State()
    waiting_for_upi_rate = State()
    waiting_for_star_username = State()
    waiting_for_star_rate = State()

# Broadcast
# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class BroadcastState(StatesGroup):
    waiting_for_message = State()

# Paid Vote Process (User Side)
# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class BuyVotes(StatesGroup):
    waiting_for_screenshot = State()
    waiting_for_amount = State()
    waiting_for_star_count = State()

# Membership System (Admin Side)
# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class AdminSettings(StatesGroup):
    waiting_for_prices = State()
    waiting_for_qr = State()

# Membership System (User Side)
# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class BuyMembership(StatesGroup):
    waiting_for_payment_proof = State()
    waiting_for_channel_link = State()
  
