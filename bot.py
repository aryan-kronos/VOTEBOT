# ==============================================================================
# 🚀 ADVANCED TELEGRAM GIVEAWAY & VOTING BOT ENGINE
# 👨‍💻 DEVELOPED & BUILT BY: ARYAN (@thatonearyan)
# 🔗 TELEGRAM CONTACT: https://t.me/thatonearyan
# 🌐 OFFICIAL DEVELOPER CHANNEL: https://t.me/thatonearyan
# 💎 CORE ARCHITECTURE & LOGIC CRAFTED BY ARYAN (@thatonearyan)
# ⚡ COPYRIGHT (C) ARYAN - ALL RIGHTS RESERVED - https://t.me/thatonearyan
# ==============================================================================

import asyncio
import logging
import random
import string
import re
from datetime import datetime, timedelta
from aiogram.types import CopyTextButton
from typing import List, Dict, Any, Optional
import pytz
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart, CommandObject
import io
import qrcode
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, PhotoSize, FSInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatMemberStatus
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.exceptions import TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import html
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, LEFT, RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR
from aiogram.types import InputMediaPhoto
from typing import Union
import os
import certifi
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'Votebot')
OWNER_IDS = [int(x.strip()) for x in os.getenv('ADMINS', '233444460,8295433038,8021449673').split(',') if x.strip()]
BOTUSER = os.getenv('BOT_USERNAME', 'Bitzvotebot')
ADMIN_IDS = OWNER_IDS
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID', '0')) if os.getenv('LOG_CHANNEL_ID') else None
BOT_NAME = os.getenv('BOT_NAME', 'BITZ GIVEAWAY BOT')
BOT_NAME_STYLED = os.getenv('BOT_NAME_STYLED', '𝐁𝐈𝐓𝐙 𝐆𝐈𝐕𝐄𝐀𝐖𝐀𝐘 𝐁𝐎𝐓!')
BRAND_NAME = os.getenv('BRAND_NAME', 'BITZ')
BRAND_NAME_SMALLCAPS = os.getenv('BRAND_NAME_SMALLCAPS', 'ʙɪᴛᴢ')
NETWORK_NAME = os.getenv('NETWORK_NAME', 'ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ')
NETWORK_USERNAME = os.getenv('NETWORK_USERNAME', 'tgbitz')
NETWORK_URL = os.getenv('NETWORK_URL', f'https://t.me/{NETWORK_USERNAME}')
SUPPORT_NAME = os.getenv('SUPPORT_NAME', 'ᴅᴇᴠᴀɴꜱʜ')
SUPPORT_USERNAME = os.getenv('SUPPORT_USERNAME', 'tgbitz_op')
SUPPORT_URL = os.getenv('SUPPORT_URL', f'https://t.me/{SUPPORT_USERNAME}')
DEVELOPER_NAME = 'ᴀʀʏᴀɴ'
DEVELOPER_USERNAME = 'thatonearyan'
DEVELOPER_URL = 'https://t.me/thatonearyan'
HOW_TO_USE_URL = os.getenv('HOW_TO_USE_URL', NETWORK_URL)
VOTE_IM = os.getenv('VOTE_IMAGE_URL', 'https://files.catbox.moe/mkfcpr.jpg')
PARTI_IMG = os.getenv('PARTICIPANT_IMAGE_URL', 'https://files.catbox.moe/27qumy.jpg')
DEFAULT_UPI_ID = os.getenv('DEFAULT_UPI_ID', 'devanshsingh2@fam')
POWERED_BY_TEXT = f"<tg-emoji emoji-id='5949775417274536507'>⚡️</tg-emoji> <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ:</b> <a href='{NETWORK_URL}'>{NETWORK_NAME}</a> | <a href='{DEVELOPER_URL}'>{DEVELOPER_NAME}</a> <tg-emoji emoji-id='5269617636001460986'>👨\u200d💻</tg-emoji>"
BRAND_FOOTER = f"✈️———— <b>{BRAND_NAME_SMALLCAPS}</b> ————✈️\n<tg-emoji emoji-id='5949775417274536507'>⚡️</tg-emoji> <b>ᴘᴏᴡᴇʀᴇᴅ</b> : <a href='{NETWORK_URL}'>{NETWORK_NAME}</a> <tg-emoji emoji-id='5949775417274536507'>💙</tg-emoji>\n<tg-emoji emoji-id='6336811288437460963'>❤️</tg-emoji> <b>ꜱᴜᴘᴘᴏʀᴛ</b> :- <a href='{SUPPORT_URL}'>{SUPPORT_NAME}</a> <tg-emoji emoji-id='5949775417274536507'>💙</tg-emoji>\n<tg-emoji emoji-id='5269617636001460986'>👨\u200d💻</tg-emoji> <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ</b> :- <a href='{DEVELOPER_URL}'>{DEVELOPER_NAME}</a> <tg-emoji emoji-id='5325547803936572038'>✨</tg-emoji>"
WELCOME_IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'welcome.jpg')
_cached_welcome_file_id = None

# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
def get_welcome_image():
    global _cached_welcome_file_id
    if _cached_welcome_file_id:
        return _cached_welcome_file_id
    if os.path.exists(WELCOME_IMAGE_PATH):
        return FSInputFile(WELCOME_IMAGE_PATH, filename='welcome.jpg')
    return 'https://files.catbox.moe/27qumy.jpg'

# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
def generate_upi_qr(upi_id: str, amount: str=None, note: str='VIP Membership') -> bytes:
    upi_uri = f'upi://pay?pa={upi_id}&pn=Devansh&cu=INR'
    if amount:
        upi_uri += f'&am={amount}'
    if note:
        upi_uri += f'&tn={note}'
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()
VOTE_IM = 'https://files.catbox.moe/mkfcpr.jpg'
PARTI_IMG = 'https://files.catbox.moe/27qumy.jpg'
IST = pytz.timezone('Asia/Kolkata')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
mongo_client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
db = mongo_client[DATABASE_NAME]
giveaways_col = db['giveaways']
votes_col = db['votes']
participants_col = db['participants']
users_col = db['users']
transactions_col = db['transactions']
settings_col = db['settings']
channels_col = db['channels']
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)
scheduler = AsyncIOScheduler(timezone=IST)
start_settings_col = db['start_settings']
membership_settings_col = db['membership_settings']
user_global_channels_col = db['user_global_channels']

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class CreateGiveaway(StatesGroup):
    waiting_for_description = State()
    waiting_for_target_channel = State()
    waiting_for_target_link = State()
    waiting_for_thumbnail = State()
    waiting_for_extra_channel = State()
    waiting_for_end_type = State()
    waiting_for_end_time = State()
    waiting_for_paid_status = State()
    waiting_for_currency_type = State()
    waiting_for_inr_qr = State()
    waiting_for_star_username = State()
    waiting_for_rates = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class BuyVotes(StatesGroup):
    waiting_for_method = State()
    waiting_for_amount = State()
    waiting_for_proof = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class SetJoin(StatesGroup):
    waiting_for_input = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class SetStart(StatesGroup):
    waiting_for_text = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class PostMaker(StatesGroup):
    waiting_for_media = State()
    waiting_for_caption = State()
    waiting_for_buttons = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class BuyMembership(StatesGroup):
    waiting_for_plan = State()
    waiting_for_proof = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class SetPrice(StatesGroup):
    waiting_for_input = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class AdminGift(StatesGroup):
    waiting_for_user = State()
    waiting_for_days = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class SetUserGlobal(StatesGroup):
    waiting_for_input = State()

# --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
class AdminSettings(StatesGroup):
    waiting_for_upi = State()
    waiting_for_qr_photo = State()
    waiting_for_prices = State()
    waiting_for_mem_text = State()
    waiting_for_start_text = State()
    waiting_for_banner_photo = State()

# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
def generate_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def is_user_member(user_id: int, channel_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except Exception:
        return False

# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
def get_message_link(chat_username: str, chat_id: int, message_id: int) -> str:
    if chat_username:
        return f'https://t.me/{chat_username}/{message_id}'
    else:
        clean_id = str(chat_id).replace('-100', '')
        return f'https://t.me/c/{clean_id}/{message_id}'

# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def get_membership(user_id: int):
    """Returns membership data if active, else None"""
    user = await users_col.find_one({'user_id': user_id})
    if not user or not user.get('membership_expiry'):
        return None
    expiry = user['membership_expiry']
    if expiry.tzinfo is None:
        expiry = IST.localize(expiry)
    if expiry > datetime.now(IST):
        return user
    return None

# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def clean_expired_global_channels():
    """Removes user force-joins if membership expired"""
    async for doc in user_global_channels_col.find({}):
        user = await get_membership(doc['user_id'])
        if not user:
            await user_global_channels_col.delete_one({'_id': doc['_id']})

# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def run_global_resync():
    """
    Runs periodically.
    Iterates through active giveaways, validates voter memberships, 
    removes invalid votes, and updates the UI with 'Must Join' buttons preserved.
    """
    logging.info("<tg-emoji emoji-id='5375338737028841420'><tg-emoji emoji-id='5375338737028841420'>♻️</tg-emoji>️</tg-emoji> [Global Resync] Starting check cycle...")
    try:
        async for ga in giveaways_col.find({'status': 'active'}):
            ga_id = ga.get('ga_id')
            creator_id = ga.get('creator_id')
            target_id = ga.get('target_channel_id')
            if not ga_id or not target_id:
                continue
            required_channels = [{'id': target_id}]
            extras = ga.get('extra_channel') or ga.get('extra_channels')
            if extras:
                if isinstance(extras, list):
                    required_channels.extend(extras)
                elif isinstance(extras, dict):
                    required_channels.append(extras)
            async for vote in votes_col.find({'ga_id': ga_id}):
                voter_id = vote.get('voter_id')
                participant_id = vote.get('participant_id')
                if not voter_id or not participant_id:
                    continue
                is_valid_member = True
                voter_user_obj = None
                for ch in required_channels:
                    try:
                        member = await bot.get_chat_member(chat_id=ch['id'], user_id=voter_id)
                        voter_user_obj = member.user
                        if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                            is_valid_member = False
                            break
                    except Exception:
                        continue
                await asyncio.sleep(0.05)
                if not is_valid_member:
                    await votes_col.delete_one({'_id': vote['_id']})
                    await participants_col.update_one({'ga_id': ga_id, 'user_id': participant_id}, {'$inc': {'vote_count': -1}})
                    p_data = await participants_col.find_one({'ga_id': ga_id, 'user_id': participant_id})
                    if not p_data:
                        continue
                    voter_name = voter_user_obj.full_name if voter_user_obj else f'ID: {voter_id}'
                    new_count = p_data.get('vote_count', 0)
                    if p_data.get('msg_id'):
                        try:
                            chan_kb = InlineKeyboardBuilder()
                            if extras:
                                if isinstance(extras, dict):
                                    extras = [extras]
                                for ch in extras:
                                    chan_kb.button(text=f"<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> Join {ch.get('title', 'Channel')}", url=ch['link'])
                            chan_kb.button(text=f"<tg-emoji emoji-id='5409029744693897259'>🗳</tg-emoji> Vote ({new_count})", callback_data=f'vote_{participant_id}_{ga_id}')
                            chan_kb.adjust(1)
                            await bot.edit_message_reply_markup(chat_id=target_id, message_id=p_data['msg_id'], reply_markup=chan_kb.as_markup())
                        except Exception:
                            pass
                    try:
                        log_text = f"<tg-emoji emoji-id='5375338737028841420'><tg-emoji emoji-id='5375338737028841420'>♻️</tg-emoji>️</tg-emoji> <b>Auto-Resync: Vote Removed</b>\n<blockquote><tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> <b>User:</b> {html.quote(voter_name)} left the channel.</blockquote>\n<blockquote><tg-emoji emoji-id='5395695537687123235'>📉</tg-emoji> <b>Participant:</b> {html.quote(p_data.get('name', 'Unknown'))}</blockquote>\n<blockquote><tg-emoji emoji-id='5395444784611480792'>📰</tg-emoji> Updated Votes: {new_count}</blockquote>"
                        log_msg = await bot.send_message(chat_id=target_id, text=log_text, disable_notification=True)
                        asyncio.create_task(delete_after_delay(target_id, log_msg.message_id, 60))
                    except Exception:
                        pass
                    try:
                        p_dm = f"<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> <b>Vote Deduction Alert!</b>\n\nA user ({html.quote(voter_name)}) left the required channel.\nYour vote count has been reduced.\n<tg-emoji emoji-id='5395695537687123235'>📉</tg-emoji> <b>New Count:</b> {new_count}"
                        await bot.send_message(chat_id=participant_id, text=p_dm)
                    except:
                        pass
                    try:
                        c_dm = f"<tg-emoji emoji-id='5395695537687123235'>🚨</tg-emoji> <b>Voter Left - Vote Removed</b>\n━━━━━━━━━━━━━━━━━━\n<tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> <b>Voter:</b> {html.quote(voter_name)}\n<tg-emoji emoji-id='5395695537687123235'>📉</tg-emoji> <b>Affected:</b> {html.quote(p_data.get('name'))} (ID: {participant_id})\n<tg-emoji emoji-id='5397782960512444700'>📌</tg-emoji> <b>Giveaway:</b> <code>{ga_id}</code>\n━━━━━━━━━━━━━━━━━━"
                        await bot.send_message(chat_id=creator_id, text=c_dm)
                    except:
                        pass
    except Exception as e:
        logging.error(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Global Resync Error: {e}")
    logging.info("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> [Global Resync] Cycle Complete.")

# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def delete_after_delay(chat_id: int, message_id: int, delay: int):
    """Deletes a message after the specified delay in seconds."""
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception:
        pass

@router.message(Command('setwin'))
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def set_win_text_command(message: Message):
    full_html = message.html_text
    try:
        _, new_template = full_html.split(maxsplit=1)
    except ValueError:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Please provide the text.\nExample: <code>/setwin <tg-emoji emoji-id='5204046146955153467'>🏆</tg-emoji> Winner is:\n\n{winners}</code>")
        return
    if '{winners}' not in new_template:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Error:</b> You must include the <code>{winners}</code> placeholder in your text.\nThis tells the bot where to list the users.")
        return
    await settings_col.update_one({'_id': 'global_win_template'}, {'$set': {'text': new_template}}, upsert=True)
    await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Win Message updated!</b>\n\n<b>Preview of format:</b>\n{new_template}\n\n<i>The bot will replace {{winners}} with the actual list.</i>")

# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def auto_end_giveaway(ga_id: str):
    """Function called by scheduler to end giveaway automatically"""
    await end_giveaway_logic(ga_id, is_auto=True)

# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def end_giveaway_logic(ga_id: str, is_auto: bool=False):
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if not ga or ga['status'] == 'ended':
        return
    await giveaways_col.update_one({'ga_id': ga_id}, {'$set': {'status': 'ended'}})
    top_participants = await participants_col.find({'ga_id': ga_id}).sort('vote_count', -1).limit(3).to_list(None)
    winners_text_block = ''
    if top_participants:
        for idx, p in enumerate(top_participants, 1):
            safe_name = html.quote(p['name'])
            winners_text_block += f"{idx}. {safe_name} - <b>{p['vote_count']} votes</b>\n"
    else:
        winners_text_block = 'No participants found.'
    settings = await settings_col.find_one({'_id': 'global_win_template'})
    if settings and settings.get('text'):
        template = settings['text']
    else:
        template = f"<tg-emoji emoji-id='5204046146955153467'>🏆</tg-emoji> <b>GIVEAWAY ENDED!</b> <tg-emoji emoji-id='5204046146955153467'>🏆</tg-emoji>\n\n<b><tg-emoji emoji-id='5204046146955153467'>🥇</tg-emoji> Top 3 Winners:</b>\n{{winners}}\n\n<i>Thank you for participating!</i>\n\n{POWERED_BY_TEXT}"
    final_caption = template.replace('{winners}', winners_text_block)
    try:
        await bot.send_message(chat_id=ga['target_channel_id'], text=final_caption, disable_web_page_preview=True)
    except Exception as e:
        logger.error(f'Failed to post results to channel: {e}')
    try:
        creator_text = f"<tg-emoji emoji-id='5395695537687123235'>🚨</tg-emoji> <b>Giveaway {ga_id} has ended {('automatically' if is_auto else 'manually')}.</b>\n\nResults posted to channel."
        await bot.send_message(chat_id=ga['creator_id'], text=creator_text)
    except:
        pass

@router.message(CommandStart())
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def cmd_start(message: Message, command: CommandObject):
    if message.from_user.id not in OWNER_IDS:
        if not await check_force_sub(message.from_user.id, message):
            return
    args = command.args
    user = message.from_user
    await users_col.update_one({'user_id': user.id}, {'$set': {'first_name': user.first_name, 'username': user.username}}, upsert=True)
    if not args:
        try:
            await bot.send_message(chat_id=LOG_CHANNEL_ID, text=f'<b>New User Started Bot</b>\n\nUser: {user.mention_html()}\nID: <code>{user.id}</code>\n\n• @{BOTUSER}')
        except Exception:
            pass
        custom_data = await start_settings_col.find_one({'type': 'start_msg'})
        if custom_data and custom_data.get('text'):
            caption_text = custom_data['text']
        else:
            caption_text = f"<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <a href='https://t.me/{BOTUSER}'><b>{BOT_NAME_STYLED}</b></a> <tg-emoji emoji-id='5461151367559141950'>🎉</tg-emoji>\n\n<blockquote expandable><tg-emoji emoji-id='5325547803936572038'>✨</tg-emoji> ꜰᴜʟʟʏ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ &amp; ꜰᴀɪʀ ɢɪᴠᴇᴀᴡᴀʏ ꜱʏꜱᴛᴇᴍ <tg-emoji emoji-id='6339289076545358952'>✔️</tg-emoji>\n<tg-emoji emoji-id='5949775417274536507'>⚡️</tg-emoji> ꜰᴀꜱᴛ &amp; ᴛʀᴀɴꜱᴘᴀʀᴇɴᴛ ᴡɪɴɴᴇʀ ꜱᴇʟᴇᴄᴛɪᴏɴ <tg-emoji emoji-id='6339289076545358952'>✔️</tg-emoji>\n<tg-emoji emoji-id='5251203410396458957'>🛡</tg-emoji> ꜱᴇᴄᴜʀᴇ, ʀᴇʟɪᴀʙʟᴇ &amp; ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ <tg-emoji emoji-id='6339289076545358952'>✔️</tg-emoji>\n<tg-emoji emoji-id='5461151367559141950'>🎊</tg-emoji> ʜᴏꜱᴛ ɢɪᴠᴇᴀᴡᴀʏꜱ ᴡɪᴛʜ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴇxᴘᴇʀɪᴇɴᴄᴇ <tg-emoji emoji-id='6339289076545358952'>✔️</tg-emoji></blockquote>\n\n<blockquote><tg-emoji emoji-id='5397916757333654639'>➕</tg-emoji> ᴛᴀᴘ <b>ɴᴇᴡ ɢɪᴠᴇᴀᴡᴀʏ</b> ʙᴜᴛᴛᴏɴ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀ ɢɪᴠᴇᴀᴡᴀʏ. <tg-emoji emoji-id='5438496463044752972'>⭐</tg-emoji></blockquote>\n<blockquote><tg-emoji emoji-id='5204046146955153467'>🎁</tg-emoji> ᴛᴀᴘ <b>ᴍʏ ɢɪᴠᴇᴀᴡᴀʏs</b> ʙᴜᴛᴛᴏɴ ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ɢɪᴠᴇᴀᴡᴀʏs. <tg-emoji emoji-id='5438496463044752972'>⭐️</tg-emoji></blockquote>\n\n{BRAND_FOOTER}"
        kb = InlineKeyboardBuilder()
        kb.button(text=f'New Giveaway', callback_data='create_ga', style='primary', icon_custom_emoji_id='5409029744693897259')
        kb.button(text=f'My Giveaways', callback_data='my_ga', style='primary', icon_custom_emoji_id='5204046146955153467')
        kb.button(text='How to Use', url=HOW_TO_USE_URL, style='primary', icon_custom_emoji_id='5269617636001460986')
        kb.button(text='Developer (Aryan)', url='https://t.me/thatonearyan', style='primary', icon_custom_emoji_id='5269617636001460986')
        kb.button(text='Add Channel', url=f'https://t.me/{BOTUSER}?startchannel=m&admin=post_messages+invite_users,startgroup=m&invite_users', style='primary', icon_custom_emoji_id='5397916757333654639')
        kb.button(text='Add Group', url=f'https://t.me/{BOTUSER}?startgroup=m&admin=invite_users', style='primary', icon_custom_emoji_id='5397916757333654639')
        kb.button(text='Membership', callback_data='membership', style='danger', icon_custom_emoji_id='5949775417274536507')
        kb.button(text='Create Post', callback_data='create_post_start', style='success', icon_custom_emoji_id='6336811288437460963')
        if user.id in ADMIN_IDS:
            kb.button(text='Settings', callback_data='admin_settings_menu', style='primary', icon_custom_emoji_id='5341715473882955310')
            kb.adjust(2, 2, 2, 1, 1, 1)
        else:
            kb.adjust(2, 2, 2, 1, 1)
        try:
            sent_msg = await message.answer_photo(photo=get_welcome_image(), has_spoiler=True, caption=caption_text, reply_markup=kb.as_markup())
            global _cached_welcome_file_id
            if sent_msg.photo and (not _cached_welcome_file_id):
                _cached_welcome_file_id = sent_msg.photo[-1].file_id
        except Exception as e:
            logger.error(f'Error sending welcome photo: {e}')
            await message.answer(text=caption_text, reply_markup=kb.as_markup())
        return
    await handle_participation_flow(message, user, args)

@router.callback_query(F.data == 'back_to_start')
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def back_to_start(call: CallbackQuery):
    await call.message.delete()
    await cmd_start(call.message, CommandObject(prefix='/', command='start', args=None))

# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def check_force_sub(user_id: int, message: Message=None):
    settings = await settings_col.find_one({'type': 'force_join'})
    channels = settings.get('channels', []) if settings else []
    async for u_ch in user_global_channels_col.find({}):
        mem = await get_membership(u_ch['user_id'])
        if mem:
            channels.append(u_ch['channel'])
    if not channels:
        return True
    missing_channels = []
    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch['id'], user_id=user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                missing_channels.append(ch)
        except Exception:
            pass
    if not missing_channels:
        return True
    if message:
        kb = InlineKeyboardBuilder()
        for ch in missing_channels:
            link = ch.get('link', '')
            if link:
                kb.button(text='📢 Join Channel', url=link)
        kb.adjust(2, 1)
        kb.button(text='✅ Verify Join', callback_data='verify_bot_fsub', style='primary')
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>🛑</tg-emoji> <b>Access Denied</b>\n\nTo use this bot, you must join our official channels first.", reply_markup=kb.as_markup())
    return False

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'verify_bot_fsub')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def verify_bot_fsub(call: CallbackQuery):
    is_joined = await check_force_sub(call.from_user.id, message=None)
    if is_joined:
        await call.message.delete()
        await call.message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Verified!</b> Type /start to continue.")
    else:
        await call.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> You haven't joined all channels yet!", show_alert=True)

# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def ask_target_channel(message: Union[Message, CallbackQuery], state: FSMContext, page: int=0):
    """
    Rewritten Target Channel logic with a Professional Paginated Selector.
    Replaces the manual prompt with a list of verified admin channels.
    """
    user_id = message.from_user.id
    ITEMS_PER_PAGE = 5
    unique_chats = {}
    async for ch in channels_col.find({'added_by': user_id}):
        unique_chats[ch['chat_id']] = ch['title']
    async for ga in giveaways_col.find({'creator_id': user_id}):
        c_id = ga.get('target_channel_id')
        if c_id and c_id not in unique_chats:
            unique_chats[c_id] = ga.get('target_channel_title', 'Recent Channel')
    valid_chats = []
    for ch_id, title in unique_chats.items():
        try:
            bot_m = await bot.get_chat_member(ch_id, bot.id)
            if bot_m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                valid_chats.append({'id': ch_id, 'title': title})
        except:
            continue
    total_pages = (len(valid_chats) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page = max(0, min(page, total_pages - 1)) if total_pages > 0 else 0
    start, end = (page * ITEMS_PER_PAGE, (page + 1) * ITEMS_PER_PAGE)
    current_batch = valid_chats[start:end]
    kb = InlineKeyboardBuilder()
    for chat in current_batch:
        kb.button(text=f"<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> {chat['title']}", callback_data=f"sel_target_{chat['id']}", style='primary')
    kb.adjust(1)
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text='⬅️️ Previous', callback_data=f'pg_target_{page - 1}', style='danger'))
    if total_pages > 1:
        nav_row.append(InlineKeyboardButton(text=f'{page + 1}/{total_pages}', callback_data='ignore'))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text='Next ➡️️', callback_data=f'pg_target_{page + 1}', style='success'))
    if nav_row:
        kb.row(*nav_row)
    kb.row(InlineKeyboardButton(text='✍️ Enter Manually', callback_data='man_target', style='primary'))
    mem = await get_membership(user_id)
    back_cb = 'back_to_extras' if mem else 'back_to_desc'
    kb.row(InlineKeyboardButton(text='🔙 Back', callback_data=back_cb))
    header = "<tg-emoji emoji-id='5397782960512444700'>🎯</tg-emoji> <b>Select Target Channel</b>"
    desc = 'Choose the channel where the giveaway will be posted.\n<i>Only channels where I am an Admin are shown below.</i>'
    final_text = f'{header}\n\n{desc}\n\n<b>Found:</b> {len(valid_chats)} Channels'
    if isinstance(message, Message):
        await message.answer(final_text, reply_markup=kb.as_markup())
    else:
        try:
            await message.edit_text(final_text, reply_markup=kb.as_markup())
        except:
            await message.message.answer(final_text, reply_markup=kb.as_markup())

@router.callback_query(F.data == 'create_ga')
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def start_create_ga(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text = "<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Create New Giveaway: Step 1</b>\n\n<b>Enter Giveaway Description</b>\nSend a short, catchy title for your event.\n<i>(e.g., 'iPhone 15 Contest', 'Best Photo 2024')</i>\n\n<blockquote><tg-emoji emoji-id='5325547803936572038'>💡</tg-emoji> Type /skip to use default: 'Vote for your favorite!'</blockquote>"
    kb = InlineKeyboardBuilder()
    kb.button(text='❌ Cancel', callback_data='back_to_start', style='danger')
    await call.message.edit_caption(caption=text, reply_markup=kb.as_markup())
    await state.set_state(CreateGiveaway.waiting_for_description)

@router.message(CreateGiveaway.waiting_for_description)
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def set_desc(message: Message, state: FSMContext):
    desc = message.text.strip() if message.text != '/skip' else 'Vote for your favorite!'
    if len(desc) > 200:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Description is too long. Please keep it under 200 characters.")
        return
    await state.update_data(description=desc)
    mem = await get_membership(message.from_user.id)
    if mem:
        text = "<tg-emoji emoji-id='5409029744693897259'>🖼</tg-emoji> <b>Custom Thumbnail (Premium)</b>\n\nSend an image to use as the banner for this giveaway.\nThis makes your post look more professional.\n\n<blockquote>Type /skip to use the default bot image.</blockquote>"
        kb = InlineKeyboardBuilder()
        kb.button(text='🔙 Back', callback_data='back_to_desc', style='danger')
        await message.answer(text, reply_markup=kb.as_markup())
        await state.set_state(CreateGiveaway.waiting_for_thumbnail)
    else:
        await ask_target_channel(message, state)

@router.callback_query(F.data == 'back_to_desc')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def back_to_desc_handler(call: CallbackQuery, state: FSMContext):
    await start_create_ga(call, state)

# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def render_channel_selector(message: Union[Message, CallbackQuery], state: FSMContext, page: int, mode: str):
    """
    Renders a professional UI listing channels where the user and bot are admins.
    mode: 'target' or 'extra'
    """
    user_id = message.from_user.id
    ITEMS_PER_PAGE = 5
    unique_chats = {}
    async for ch in channels_col.find({'added_by': user_id}):
        unique_chats[ch['chat_id']] = ch['title']
    async for ga in giveaways_col.find({'creator_id': user_id}):
        c_id = ga.get('target_channel_id')
        if c_id and c_id not in unique_chats:
            unique_chats[c_id] = ga.get('target_channel_title', str(c_id))
    valid_chats = []
    all_ids = sorted(unique_chats.keys())
    for ch_id in all_ids:
        try:
            bot_member = await bot.get_chat_member(ch_id, bot.id)
            if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                continue
            user_member = await bot.get_chat_member(ch_id, user_id)
            if user_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                continue
            valid_chats.append({'id': ch_id, 'title': unique_chats[ch_id]})
        except:
            continue
    total_items = len(valid_chats)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if page >= total_pages:
        page = max(0, total_pages - 1)
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_batch = valid_chats[start_idx:end_idx]
    kb = InlineKeyboardBuilder()
    for chat in current_batch:
        kb.button(text=f"<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> {chat['title']}", callback_data=f"sel_{mode}_{chat['id']}")
    kb.adjust(1)
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton(text='⬅️️ Prev', callback_data=f'pg_{mode}_{page - 1}'))
    if total_pages > 1:
        nav_btns.append(InlineKeyboardButton(text=f"<tg-emoji emoji-id='5395444784611480792'>📄</tg-emoji> {page + 1}/{total_pages}", callback_data='ignore'))
    if page < total_pages - 1:
        nav_btns.append(InlineKeyboardButton(text='Next ➡️️', callback_data=f'pg_{mode}_{page + 1}'))
    if nav_btns:
        kb.row(*nav_btns)
    if mode == 'extra':
        kb.row(InlineKeyboardButton(text='⏭ Skip Extra Channel', callback_data='skip_extra'))
    back_cb = 'back_to_desc' if mode == 'extra' else 'back_to_extras'
    if mode == 'target' and (not await get_membership(user_id)):
        back_cb = 'back_to_desc'
    kb.row(InlineKeyboardButton(text='🔙 Back', callback_data=back_cb))
    if mode == 'target':
        header = "<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> <b>Select Target Channel</b>"
        desc = 'Choose where the giveaway post will be published.\n<i>I must be an admin there!</i>'
    else:
        header = "<tg-emoji emoji-id='5397916757333654639'>➕</tg-emoji> <b>Select Extra Channel</b> (Optional)"
        desc = 'Users must join this channel to vote.\n<i>Limit: 1 Channel (Premium)</i>'
    final_text = f'{header}\n\n{desc}'
    if isinstance(message, Message):
        await message.answer(final_text, reply_markup=kb.as_markup())
    else:
        try:
            await message.message.edit_text(final_text, reply_markup=kb.as_markup())
        except:
            await message.message.delete()
            await message.message.answer(final_text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('pg_'))
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def handle_selector_pagination(call: CallbackQuery, state: FSMContext):
    parts = call.data.split('_')
    mode = parts[1]
    page = int(parts[2])
    await render_channel_selector(call, state, page, mode)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'ignore')
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def ignore_callback(call: CallbackQuery):
    await call.answer()

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(CreateGiveaway.waiting_for_thumbnail)
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def set_ga_thumbnail(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(custom_thumb=message.photo[-1].file_id)
    elif message.text == '/skip':
        await state.update_data(custom_thumb=None)
    else:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Please send a <b>Photo</b> or type <code>/skip</code>.")
        return
    await state.update_data(extra_channels=[])
    await render_channel_selector(message, state, 0, 'extra')

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('sel_extra_'))
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def select_extra_channel(call: CallbackQuery, state: FSMContext):
    ch_id = int(call.data.split('_')[2])
    try:
        chat = await bot.get_chat(ch_id)
        link = chat.invite_link
        if not link:
            link = await bot.export_chat_invite_link(ch_id)
        channel_data = [{'id': ch_id, 'link': link, 'title': chat.title}]
        await state.update_data(extra_channels=channel_data)
        await call.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> Channel Selected!")
        await ask_target_channel_flow(call, state)
    except Exception as e:
        await call.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Error generating link: {e}", show_alert=True)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'skip_extra')
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def skip_extra_channel(call: CallbackQuery, state: FSMContext):
    await state.update_data(extra_channels=[])
    await ask_target_channel_flow(call, state)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'man_extra')
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def manual_extra_prompt(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Enter Extra Channel Manually</b>\n\nFormat: <code>ChannelID InviteLink</code>\nExample: <code>-10012345678 https://t.me/...</code>\n\n<i>Note: I must be an admin there!</i>", reply_markup=InlineKeyboardBuilder().button(text='🔙 Back', callback_data='back_to_extra_list').as_markup())
    await state.set_state(CreateGiveaway.waiting_for_extra_channel)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'back_to_extra_list')
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def back_to_extra_list(call: CallbackQuery, state: FSMContext):
    await render_channel_selector(call, state, 0, 'extra')

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(CreateGiveaway.waiting_for_extra_channel)
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def process_manual_extra(message: Message, state: FSMContext):
    try:
        parts = message.text.strip().split()
        if len(parts) < 2:
            raise ValueError
        ex_id = int(parts[0])
        ex_link = parts[1]
        m = await bot.get_chat_member(ex_id, bot.id)
        if m.status != ChatMemberStatus.ADMINISTRATOR:
            await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> I am not admin there.")
            return
        chat = await bot.get_chat(ex_id)
        channel_data = [{'id': ex_id, 'link': ex_link, 'title': chat.title}]
        await state.update_data(extra_channels=channel_data)
        await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Extra Channel Added!</b>")
        await ask_target_channel_flow(message, state)
    except:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid format. Use: <code>ID Link</code>")

# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def ask_target_channel_flow(event, state):
    await render_channel_selector(event, state, 0, 'target')

@router.callback_query(F.data.startswith('sel_target_'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def select_target_channel(call: CallbackQuery, state: FSMContext):
    ch_id = int(call.data.split('_')[2])
    try:
        chat = await bot.get_chat(ch_id)
        link = chat.invite_link
        if not link:
            link = await bot.export_chat_invite_link(ch_id)
        await state.update_data(target_channel_id=chat.id, target_channel_title=chat.title, target_channel_username=chat.username, target_link=link)
        await ask_end_configuration(call.message, state)
    except Exception as e:
        await call.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Error getting link: {e}", show_alert=True)

@router.callback_query(F.data == 'man_target')
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def manual_target_prompt(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> <b>Enter Target Channel Manually</b>\n\nSend the <b>Username</b> (e.g., @mychannel) or <b>ID</b>.", reply_markup=InlineKeyboardBuilder().button(text='🔙 Back', callback_data='back_to_target_list').as_markup())
    await state.set_state(CreateGiveaway.waiting_for_target_channel)

@router.callback_query(F.data == 'back_to_target_list')
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def back_to_target_list(call: CallbackQuery, state: FSMContext):
    await render_channel_selector(call, state, 0, 'target')

@router.message(CreateGiveaway.waiting_for_target_channel)
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def set_channel_manual(message: Message, state: FSMContext):
    try:
        chat = await bot.get_chat(message.text.strip())
        if not await is_user_member(bot.id, chat.id):
            await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> I am not admin there.")
            return
        await state.update_data(target_channel_id=chat.id, target_channel_title=chat.title, target_channel_username=chat.username)
        await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Selected:</b> {chat.title}\n\n<tg-emoji emoji-id='5271604874419647061'>🔗</tg-emoji> <b>Send Channel Invite Link</b>\nSend the public invite link.")
        await state.set_state(CreateGiveaway.waiting_for_target_link)
    except:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Channel not found.")

@router.callback_query(F.data == 'back_to_target_select')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def back_to_target_select(call: CallbackQuery, state: FSMContext):
    await render_channel_selector(call, state, 0, 'target')

# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def ask_end_configuration(message: Message, state: FSMContext):
    text = "<tg-emoji emoji-id='5375338737028841420'>⏳</tg-emoji> <b>Giveaway Ending Configuration</b>\n\n<b><tg-emoji emoji-id='5269617636001460986'>🤖</tg-emoji> Automatic:</b> Ends automatically at a specific time.\n<b><tg-emoji emoji-id='5341715473882955310'>✋</tg-emoji> Manual:</b> You stop it manually using the panel."
    kb = InlineKeyboardBuilder()
    kb.button(text='🤖 Automatic End', callback_data='end_auto', style='success')
    kb.button(text='✋ Manual End', callback_data='end_manual', style='danger')
    kb.adjust(2)
    kb.button(text='🔙 Back', callback_data='back_to_target_select')
    if isinstance(message, Message):
        try:
            await message.edit_text(text, reply_markup=kb.as_markup())
        except:
            await message.answer(text, reply_markup=kb.as_markup())
    else:
        await message.edit_text(text, reply_markup=kb.as_markup())
    await state.set_state(CreateGiveaway.waiting_for_end_type)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'back_to_extras')
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def back_to_extras_router(call: CallbackQuery, state: FSMContext):
    await render_channel_selector(call, state, 0, 'extra')

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(CreateGiveaway.waiting_for_end_type)
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def set_end_type(call: CallbackQuery, state: FSMContext):
    mode = call.data
    await state.update_data(end_mode=mode)
    if mode == 'end_manual':
        await ask_paid_votes(call, state)
    else:
        now_str = datetime.now(IST).strftime('%d-%m-%Y %H:%M')
        text = f"<tg-emoji emoji-id='5395444784611480792'>📅</tg-emoji> <b>Set End Date & Time</b>\n\nCurrent Time (IST): <code>{now_str}</code>\n\n<b>Format:</b> <code>DD-MM-YYYY HH:MM</code>\n<i>Example:</i> <code>25-12-2025 18:00</code>"
        kb = InlineKeyboardBuilder()
        kb.button(text='🔙 Back', callback_data='back_to_end_type')
        await call.message.edit_text(text, reply_markup=kb.as_markup())
        await state.set_state(CreateGiveaway.waiting_for_end_time)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'back_to_end_type')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def back_to_end_type(call: CallbackQuery, state: FSMContext):
    await ask_end_configuration(call.message, state)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(CreateGiveaway.waiting_for_end_time)
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def set_end_time(message: Message, state: FSMContext):
    try:
        dt_str = message.text.strip()
        dt_naive = datetime.strptime(dt_str, '%d-%m-%Y %H:%M')
        dt_ist = IST.localize(dt_naive)
        if dt_ist <= datetime.now(IST):
            await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Error:</b> Time must be in the future.")
            return
        await state.update_data(end_date_iso=dt_ist.isoformat())
        await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> Will end on: <b>{dt_ist.strftime('%d %b %Y, %I:%M %p IST')}</b>")
        await ask_paid_votes(message, state)
    except ValueError:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Invalid Format.</b>\nPlease use: <code>DD-MM-YYYY HH:MM</code>")

# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def ask_paid_votes(event: Union[Message, CallbackQuery], state: FSMContext):
    text = "<tg-emoji emoji-id='5409048419211682843'>💰</tg-emoji> <b>Paid Votes Configuration</b>\n\nDo you want to allow users to buy extra votes using Money or Telegram Stars?\n<i>This generates revenue and increases vote counts.</i>"
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Enable Paid Votes', callback_data='paid_yes', style='success')
    kb.button(text='❌ Disable Paid Votes', callback_data='paid_no', style='primary')
    kb.adjust(1)
    kb.button(text='🔙 Back', callback_data='back_to_end_type', style='danger')
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=kb.as_markup())
    elif isinstance(event, Message):
        await event.answer(text, reply_markup=kb.as_markup())
    else:
        try:
            await event.message.edit_text(text, reply_markup=kb.as_markup())
        except:
            await event.answer(text, reply_markup=kb.as_markup())
    await state.set_state(CreateGiveaway.waiting_for_paid_status)

@router.callback_query(CreateGiveaway.waiting_for_paid_status)
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def set_paid_status(call: CallbackQuery, state: FSMContext):
    await call.answer()
    if call.data == 'paid_no':
        await call.message.edit_text("<tg-emoji emoji-id='5375338737028841420'>⏳</tg-emoji> <i>Processing giveaway without paid votes...</i>")
        await finalize_giveaway(call.message, state, paid_enabled=False, user_from_call=call.from_user)
    elif call.data == 'paid_yes':
        await state.update_data(paid_enabled=True)
        text = '💱 <b>Select Supported Currency</b>\n\nChoose how you want to receive payments:'
        kb = InlineKeyboardBuilder()
        kb.button(text='🇮🇳 INR (UPI/QR)', callback_data='curr_inr', style='primary')
        kb.button(text='⭐️ Telegram Stars', callback_data='curr_star', style='primary')
        kb.button(text='🔄 Both (INR & Stars)', callback_data='curr_both', style='primary')
        kb.adjust(1)
        kb.button(text='🔙 Back', callback_data='back_to_paid_ask', style='danger')
        await call.message.edit_text(text, reply_markup=kb.as_markup())
        await state.set_state(CreateGiveaway.waiting_for_currency_type)
    elif call.data == 'back_to_end_type':
        data = await state.get_data()
        text = "<tg-emoji emoji-id='5375338737028841420'>⏳</tg-emoji> <b>Ending Configuration</b>\n\nHow should this giveaway end?"
        kb = InlineKeyboardBuilder()
        kb.button(text='🤖 Automatic End', callback_data='end_auto')
        kb.button(text='✋ Manual End', callback_data='end_manual')
        kb.adjust(2)
        await call.message.edit_text(text, reply_markup=kb.as_markup())
        await state.set_state(CreateGiveaway.waiting_for_end_type)

@router.callback_query(F.data == 'back_to_paid_ask')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def back_to_paid_ask(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_paid_votes(call.message, state)

@router.callback_query(CreateGiveaway.waiting_for_currency_type)
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def set_currency(call: CallbackQuery, state: FSMContext):
    await call.answer()
    ctype = call.data
    await state.update_data(currency_type=ctype)
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Back', callback_data='back_to_paid_ask')
    if ctype in ['curr_inr', 'curr_both']:
        await call.message.edit_text("<tg-emoji emoji-id='5427168083074628963'>📸</tg-emoji> <b>Upload Payment QR Code</b>\n\nPlease send the <b>Photo</b> of your UPI/QR Code now.", reply_markup=kb.as_markup())
        await state.set_state(CreateGiveaway.waiting_for_inr_qr)
    elif ctype == 'curr_star':
        await call.message.edit_text("<tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> <b>Telegram Star Recipient</b>\n\nEnter the @username where users should send Stars.", reply_markup=kb.as_markup())
        await state.set_state(CreateGiveaway.waiting_for_star_username)

@router.message(CreateGiveaway.waiting_for_inr_qr)
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def set_qr(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Error:</b> Please send a Photo/Image of your QR code.")
        return
    file_id = message.photo[-1].file_id
    await state.update_data(qr_code=file_id)
    data = await state.get_data()
    if data['currency_type'] == 'curr_both':
        await message.answer("<tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> <b>Now enter Telegram @Username for Stars:</b>")
        await state.set_state(CreateGiveaway.waiting_for_star_username)
    else:
        await ask_rates(message, state)

@router.message(CreateGiveaway.waiting_for_star_username)
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def set_star_user(message: Message, state: FSMContext):
    username = message.text.strip()
    if not username.startswith('@'):
        username = '@' + username
    await state.update_data(star_user=username)
    await ask_rates(message, state)

# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def ask_rates(message: Message, state: FSMContext):
    data = await state.get_data()
    ctype = data.get('currency_type')
    text = "<tg-emoji emoji-id='5409029744693897259'>📊</tg-emoji> <b>Set Vote Rates</b>\n\n"
    if ctype == 'curr_inr':
        text += 'How many votes for <b>1 INR</b>?\n<i>Example: Send 10 (user gets 10 votes per 1 Rupee)</i>'
    elif ctype == 'curr_star':
        text += 'How many votes for <b>1 Star</b>?\n<i>Example: Send 5 (user gets 5 votes per 1 Star)</i>'
    else:
        text += 'Enter rates for both <b>INR</b> and <b>Stars</b>.\n<b>Format:</b> <code>INR_RATE STAR_RATE</code>\n<i>Example: Send 10 20</i>'
    await message.answer(text)
    await state.set_state(CreateGiveaway.waiting_for_rates)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(CreateGiveaway.waiting_for_rates)
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def set_rates(message: Message, state: FSMContext):
    text = message.text.strip()
    data = await state.get_data()
    ctype = data.get('currency_type')
    rates = {}
    try:
        if ctype == 'curr_inr':
            rates['inr'] = int(text)
        elif ctype == 'curr_star':
            rates['star'] = int(text)
        else:
            parts = text.split()
            if len(parts) != 2:
                raise ValueError
            rates['inr'] = int(parts[0])
            rates['star'] = int(parts[1])
        await state.update_data(rates=rates)
        await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Rates recorded!</b> Finalizing your giveaway...")
        await finalize_giveaway(message, state, paid_enabled=True)
    except ValueError:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Invalid Input:</b> Please enter numbers only.\n<i>Example: 10</i>")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'back_to_currency')
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def back_to_currency_selection(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await set_paid_status(call, state)

# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def finalize_giveaway(message: Message, state: FSMContext, paid_enabled: bool, user_from_call=None):
    try:
        data = await state.get_data()
        user = user_from_call if user_from_call else message.from_user
        ga_id = generate_id()
        description = data.get('description', 'Vote for your favorite!')
        target_id = data.get('target_channel_id')
        target_link = data.get('target_link', 'https://t.me/telegram')
        target_title = data.get('target_channel_title', 'Channel')
        target_user = data.get('target_channel_username')
        end_mode = data.get('end_mode', 'end_manual')
        custom_thumb = data.get('custom_thumb')
        extras = data.get('extra_channels') or data.get('extra_channel')
        user_mem = await get_membership(user.id)
        mem_status = "Premium <tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji>" if user_mem else "Free <tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji>"
        doc = {'ga_id': ga_id, 'creator_id': user.id, 'description': description, 'target_channel_id': target_id, 'target_channel_title': target_title, 'target_channel_username': target_user, 'target_link': target_link, 'end_mode': end_mode, 'status': 'active', 'created_at': datetime.now(), 'participants_count': 0, 'paid_enabled': paid_enabled, 'custom_thumb': custom_thumb, 'extra_channel': extras}
        if end_mode == 'end_auto' and data.get('end_date_iso'):
            doc['end_time'] = data['end_date_iso']
            dt = datetime.fromisoformat(data['end_date_iso'])
            scheduler.add_job(auto_end_giveaway, 'date', run_date=dt, args=[ga_id], id=f'job_{ga_id}', replace_existing=True)
            doc['job_id'] = f'job_{ga_id}'
        if paid_enabled:
            doc.update({'currency_type': data.get('currency_type'), 'qr_code': data.get('qr_code'), 'star_user': data.get('star_user'), 'rates': data.get('rates', {})})
        await giveaways_col.insert_one(doc)
        auto_txt = 'Manual'
        if data.get('end_date_iso'):
            auto_txt = datetime.fromisoformat(data['end_date_iso']).strftime('%d-%b %H:%M')
        log_text = f"""<tg-emoji emoji-id='5409029744693897259'>🆕</tg-emoji> <b>New Giveaway Created</b>\n━━━━━━━━━━━━━━━━━━\n<tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> <b>User:</b> {html.quote(user.full_name)}\n<tg-emoji emoji-id='5427168083074628963'>🆔</tg-emoji> <b>ID:</b> <code>{user.id}</code>\n<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> <b>Status:</b> {mem_status}\n━━━━━━━━━━━━━━━━━━\n<tg-emoji emoji-id='5409048419211682843'>💰</tg-emoji> <b>Paid:</b> {("Yes <tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji>" if paid_enabled else "No <tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji>")}\n<tg-emoji emoji-id='5375338737028841420'>⏳</tg-emoji> <b>End:</b> {auto_txt}\n<tg-emoji emoji-id='5427168083074628963'>🆔</tg-emoji> <b>GA-ID:</b> <code>{ga_id}</code>"""
        try:
            if LOG_CHANNEL_ID:
                await bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text)
        except:
            pass
        bot_info = await bot.get_me()
        link = f'https://t.me/{bot_info.username}?start={ga_id}'
        kb = InlineKeyboardBuilder()
        kb.button(text='⚙️️ Manage Giveaway', callback_data=f'manage_ga_{ga_id}', style='success')
        kb.button(text='🏆 Leaderboard', callback_data=f'leaderboard_{ga_id}', style='primary')
        kb.adjust(1)
        await message.answer(f"<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <b>Giveaway Created Successfully!</b>\n\n<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Desc:</b> {description}\n<tg-emoji emoji-id='5427168083074628963'>🆔</tg-emoji> <b>ID:</b> <code>{ga_id}</code>\n\n<tg-emoji emoji-id='5271604874419647061'>🔗</tg-emoji> <b>Participation Link:</b>\n{link}\n\n{POWERED_BY_TEXT}", reply_markup=kb.as_markup())
        await state.clear()
    except Exception as e:
        logging.error(f'Error in finalize_giveaway: {e}')
        await message.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Creation Failed:</b>\n<code>{str(e)}</code>")

@router.message(Command('setstart'))
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def cmd_setstart(message: Message, state: FSMContext):
    if message.from_user.id not in OWNER_IDS:
        return
    await message.answer("<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Send the new Start Message.</b>\n\nI will preserve all formatting (bold, italic, links, etc.).\nUse /resetstart to go back to default.")
    await state.set_state(SetStart.waiting_for_text)

@router.message(SetStart.waiting_for_text)
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def process_setstart(message: Message, state: FSMContext):
    new_text = message.html_text
    await start_settings_col.update_one({'type': 'start_msg'}, {'$set': {'text': new_text}}, upsert=True)
    await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Start message updated successfully!</b>")
    await state.clear()

@router.message(Command('resetstart'))
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def cmd_resetstart(message: Message):
    if message.from_user.id not in OWNER_IDS:
        return
    await start_settings_col.delete_one({'type': 'start_msg'})
    await message.answer("<tg-emoji emoji-id='5375338737028841420'>🔄</tg-emoji> <b>Start message reset to default.</b>")

@router.message(Command('resync'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def resync_votes(message: Message, command: CommandObject):
    """
    Checks all voters in a giveaway. If they left the channel, removes vote.
    Usage: /resync {ga_id}
    """
    ga_id = command.args
    if not ga_id:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Usage: <code>/resync {giveaway_id}</code>")
        return
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if not ga:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid Giveaway ID.")
        return

@router.message(Command('resync'))
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def resync_votes(message: Message, command: CommandObject):
    ga_id = command.args
    if not ga_id:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Usage: <code>/resync {giveaway_id}</code>")
        return
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if not ga:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid Giveaway ID.")
        return
    if message.from_user.id != ga['creator_id']:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Only the giveaway creator can use /resync.")
        return
    status_msg = await message.answer("<tg-emoji emoji-id='5375338737028841420'>⏳</tg-emoji> <b>Manual Resync Started...</b>\n<i>Validating all voters...</i>")
    req_channels = [ga['target_channel_id']]
    if ga.get('extra_channel'):
        req_channels.append(ga['extra_channel']['id'])
    removed_count = 0
    affected_participants = {}
    votes_cursor = votes_col.find({'ga_id': ga_id})
    async for vote in votes_cursor:
        voter_id = vote['voter_id']
        is_still_member = True
        for ch_id in req_channels:
            try:
                member = await bot.get_chat_member(chat_id=ch_id, user_id=voter_id)
                if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    is_still_member = False
                    break
            except:
                continue
        if not is_still_member:
            await votes_col.delete_one({'_id': vote['_id']})
            removed_count += 1
            await participants_col.update_one({'ga_id': ga_id, 'user_id': vote['participant_id']}, {'$inc': {'vote_count': -1}})
            affected_participants[vote['participant_id']] = True
    if removed_count > 0:
        for p_id in affected_participants.keys():
            p_data = await participants_col.find_one({'ga_id': ga_id, 'user_id': p_id})
            if p_data and p_data.get('msg_id'):
                try:
                    kb = InlineKeyboardBuilder()
                    kb.button(text='Join Channel', url=ga['target_link'], style='primary')
                    if ga.get('extra_channel'):
                        kb.button(text=f'Join', url=ga['extra_channel']['link'], style='primary')
                    kb.adjust(1)
                    kb.button(text=f"<tg-emoji emoji-id='5409029744693897259'>🗳</tg-emoji> Vote ({p_data['vote_count']})", callback_data=f'vote_{p_id}_{ga_id}', style='success')
                    kb.adjust(1, 1)
                    await bot.edit_message_reply_markup(chat_id=ga['target_channel_id'], message_id=p_data['msg_id'], reply_markup=kb.as_markup())
                except:
                    pass
    await status_msg.edit_text(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Resync Done!</b>\n\n<tg-emoji emoji-id='5445267414562389170'>🗑</tg-emoji> Removed: {removed_count} votes.")

@router.message(Command('setvotetext'))
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def set_vote_text_command(message: Message):
    full_html = message.html_text
    try:
        _, new_template = full_html.split(maxsplit=1)
    except ValueError:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Please provide the text after the command.\nExample: <code>/setvotetext My Caption...</code>")
        return
    await settings_col.update_one({'_id': 'global_vote_caption'}, {'$set': {'text': new_template}}, upsert=True)
    await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Vote text updated successfully!</b>\n\n<b>Preview:</b>\n{new_template}")

# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def get_missing_channels(user_id: int, ga: dict) -> list:
    """
    Checks Target + Extra Channels.
    Returns a list of missing channel dicts {id, link, title}.
    """
    required = []
    required.append({'id': ga['target_channel_id'], 'link': ga['target_link'], 'title': ga.get('target_channel_title', 'Main Channel')})
    extras = ga.get('extra_channel') or ga.get('extra_channels')
    if extras:
        if isinstance(extras, list):
            required.extend(extras)
        elif isinstance(extras, dict):
            required.append(extras)
    missing = []
    for ch in required:
        try:
            member = await bot.get_chat_member(chat_id=ch['id'], user_id=user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                missing.append(ch)
        except Exception:
            missing.append(ch)
    return missing

# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def handle_participation_flow(message: Message, user, ga_id):
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if not ga or ga['status'] != 'active':
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> <b>Giveaway Inactive</b>\nThis event has ended or is no longer available.")
        return
    if await participants_col.find_one({'ga_id': ga_id, 'user_id': user.id}):
        await send_ga_links(message, user, ga_id)
        return
    missing = await get_missing_channels(user.id, ga)
    if missing:
        kb = InlineKeyboardBuilder()
        for ch in missing:
            kb.button(text=f"<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> Join {ch.get('title', 'Channel')}", url=ch['link'])
        kb.adjust(1)
        kb.button(text='✅ I Have Joined', callback_data=f'verify_{ga_id}')
        await message.answer('👋 <b>Welcome!</b>\n\nTo enter this giveaway, you must join the required channels below first.', reply_markup=kb.as_markup())
        return
    await ask_confirmation(message, ga)

@router.callback_query(F.data.startswith('verify_'))
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def verify_callback(call: CallbackQuery):
    ga_id = call.data.split('_')[1]
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if await get_missing_channels(call.from_user.id, ga):
        await call.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> You still haven't joined all channels!", show_alert=True)
        return
    await call.message.delete()
    await ask_confirmation(call.message, ga)

# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def ask_confirmation(message: Message, ga):
    """Sends the professional confirmation prompt."""
    kb = InlineKeyboardBuilder()
    kb.button(text='🔥 Confirm & Participate', callback_data=f"confirm_join_{ga['ga_id']}", style='success')
    kb.button(text='❌ Cancel', callback_data='delete_msg', style='danger')
    await message.answer(f"<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> <b>Verification Successful</b>\n\n<b>Event:</b> {html.quote(ga.get('description', 'Giveaway'))}\n\nReady to generate your personal vote post in the target channel?", reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('confirm_join_'))
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def confirm_participation_callback(call: CallbackQuery):
    ga_id = call.data.split('_')[2]
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if await get_missing_channels(call.from_user.id, ga):
        await call.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Session Expired. Please re-verify memberships.", show_alert=True)
        return
    await call.message.delete()
    await register_participant(call.message, call.from_user, ga)

# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def register_participant(message: Message, user, ga):
    chan_kb = InlineKeyboardBuilder()
    extras = ga.get('extra_channel') or ga.get('extra_channels')
    if extras:
        if isinstance(extras, dict):
            extras = [extras]
        for ch in extras:
            chan_kb.button(text=f"<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> Join", url=ch['link'], style='primary')
    chan_kb.button(text='🗳 Vote (0)', callback_data=f"vote_{user.id}_{ga['ga_id']}", style='success')
    chan_kb.adjust(1)
    settings = await settings_col.find_one({'_id': 'global_vote_caption'})
    template = settings.get('text') if settings else "<b><tg-emoji emoji-id='5949775417274536507'>⚡️</tg-emoji> PARTICIPANT:</b> {user.full_name}\n<b>ID:</b> {user.id}"

    # --- [Class Definition: Engineered & Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)] ---
    class FormatUser:

        # [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
        def __init__(self, u):
            self.full_name = html.quote(u.full_name)
            self.id = u.id
            self.username = u.username if u.username else 'NoUser'
    try:
        caption = template.replace(" or 'NoUser'", '').format(user=FormatUser(user))
    except:
        caption = f"<tg-emoji emoji-id='5949775417274536507'>⚡️</tg-emoji> <b>Participant:</b> {html.quote(user.full_name)}"
    try:
        sent = await bot.send_photo(chat_id=ga['target_channel_id'], photo=ga.get('custom_thumb') or VOTE_IM, caption=caption, reply_markup=chan_kb.as_markup())
    except Exception as e:
        await message.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Error:</b> Could not post to target channel.\n{e}")
        return
    await participants_col.insert_one({'ga_id': ga['ga_id'], 'user_id': user.id, 'username': user.username, 'name': user.full_name, 'vote_count': 0, 'paid_votes_count': 0, 'msg_id': sent.message_id, 'channel_id': ga['target_channel_id']})
    await giveaways_col.update_one({'ga_id': ga['ga_id']}, {'$inc': {'participants_count': 1}})
    await send_ga_links(message, user, ga['ga_id'])

# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def send_ga_links(message: Message, user, ga_id):
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    p_data = await participants_col.find_one({'ga_id': ga_id, 'user_id': user.id})
    if not p_data:
        return
    post_link = get_message_link(ga.get('target_channel_username'), ga['target_channel_id'], p_data['msg_id'])
    copy_content = f"<tg-emoji emoji-id='5424972470023104089'>🔥</tg-emoji> Vote for me in the Giveaway!\n\n<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> Channel: {ga['target_link']}\n<tg-emoji emoji-id='5409029744693897259'>🗳</tg-emoji> Post Link: {post_link}\n\n<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Note: Don't leave from any channel, @{BOTUSER} uses automatic votes resync system!"
    text = f"🎊 <b>Participation Confirmed!</b>\n━━━━━━━━━━━━━━━━━━━━\n<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> <b>Target Channel:</b> <a href='{ga['target_link']}'>Open Channel</a>\n<tg-emoji emoji-id='5409029744693897259'>🗳</tg-emoji> <b>Your Vote Post:</b> <a href='{post_link}'>View My Post</a>\n━━━━━━━━━━━━━━━━━━━━\n<tg-emoji emoji-id='5325547803936572038'>✨</tg-emoji> <i>Tip: Click the button below to copy your referral details and share with friends!</i>"
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Copy Vote Link', copy_text=CopyTextButton(text=copy_content)))
    if ga.get('paid_enabled'):
        kb.row(InlineKeyboardButton(text='💰 Buy Paid Votes', callback_data=f'buy_start_{ga_id}', style='success'))
    kb.row(InlineKeyboardButton(text='🏆 Leaderboard', callback_data=f'leaderboard_{ga_id}', style='primary'))
    kb.adjust(1)
    kb.row(InlineKeyboardButton(text='🔄 Get Links Again', callback_data=f'get_links_{ga_id}', style='primary'))
    kb.adjust(1, 1, 1)
    if isinstance(message, Message):
        await message.answer_photo(photo=PARTI_IMG, has_spoiler=True, caption=text, reply_markup=kb.as_markup())
    else:
        await message.answer_photo(photo=PARTI_IMG, has_spoiler=True, caption=text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('get_links_'))
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def callback_get_links(call: CallbackQuery):
    ga_id = call.data.split('_')[2]
    await call.answer("<tg-emoji emoji-id='5375338737028841420'>🔄</tg-emoji> Refreshing your links...")
    await send_ga_links(call.message, call.from_user, ga_id)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('setprices'))
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def cmd_setprices(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    args = message.text.split()[1:]
    if not args or len(args) % 2 != 0:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Usage: <code>/setprices 1D 20 7D 70 30D 80</code>\n(DayCount Price DayCount Price...)")
        return
    plans = []
    try:
        for i in range(0, len(args), 2):
            label = args[i].upper()
            price = args[i + 1]
            days = int(label.replace('D', ''))
            plans.append({'label': label, 'days': days, 'price': price})
        await membership_settings_col.update_one({'type': 'plans'}, {'$set': {'plans': plans}}, upsert=True)
        await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Membership Plans Updated!</b>")
    except ValueError:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Error: Days must be numbers (e.g. 1D) and Price must be numbers.")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('setupi'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def cmd_setupi(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Usage: <code>/setupi devanshsingh2@fam</code>")
        return
    upi_id = args[1].strip()
    await membership_settings_col.update_one({'type': 'qr'}, {'$set': {'upi_id': upi_id, 'file_id': None}}, upsert=True)
    await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Payment UPI ID set to:</b> <code>{upi_id}</code>\nDynamic QR codes will now be generated for this UPI ID!")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('setqr'))
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def cmd_setqr(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        upi_id = args[1].strip()
        await membership_settings_col.update_one({'type': 'qr'}, {'$set': {'upi_id': upi_id, 'file_id': None}}, upsert=True)
        await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Payment UPI ID set to:</b> <code>{upi_id}</code>\nDynamic QR codes enabled!")
        return
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Usage:\n1. <code>/setqr your_upi@id</code> (for dynamic QR)\n2. Reply to a photo with <code>/setqr</code> (for custom fixed QR image)")
        return
    file_id = message.reply_to_message.photo[-1].file_id
    await membership_settings_col.update_one({'type': 'qr'}, {'$set': {'file_id': file_id}}, upsert=True)
    await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Static QR Code Image Updated!</b>")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'admin_settings_menu')
@router.message(Command('settings'))
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def show_admin_settings(event: Union[Message, CallbackQuery], state: FSMContext):
    user_id = event.from_user.id
    if user_id not in ADMIN_IDS:
        if isinstance(event, CallbackQuery):
            await event.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Unauthorized.", show_alert=True)
        return
    await state.clear()
    qr_data = await membership_settings_col.find_one({'type': 'qr'})
    current_upi = qr_data.get('upi_id', 'devanshsingh2@fam') if qr_data else 'devanshsingh2@fam'
    settings = await membership_settings_col.find_one({'type': 'plans'})
    plans_summary = ', '.join([f"{p['label']}: ₹{p['price']}" for p in settings['plans']]) if settings and settings.get('plans') else '7D: ₹49, 15D: ₹89, 30D: ₹149'
    panel_text = f"<tg-emoji emoji-id='5341715473882955310'>⚙️</tg-emoji> <b>ADMIN CONTROL PANEL</b>\n━━━━━━━━━━━━━━━━━━━━\n<tg-emoji emoji-id='5409048419211682843'>💳</tg-emoji> <b>UPI ID:</b> <code>{current_upi}</code> (QR generates automatically)\n<tg-emoji emoji-id='5438496463044752972'>💎</tg-emoji> <b>VIP Plans:</b> {plans_summary}\n\n<i>Tap any button below to configure directly from Telegram:</i>"
    kb = InlineKeyboardBuilder()
    kb.button(text='Change UPI ID', callback_data='admin_set_upi', icon_custom_emoji_id='5409048419211682843')
    kb.button(text='Edit Plan Prices', callback_data='admin_set_prices', icon_custom_emoji_id='5409048419211682843')
    kb.button(text='Edit VIP Text', callback_data='admin_set_memtext', icon_custom_emoji_id='5427168083074628963')
    kb.button(text='Edit Welcome Text', callback_data='admin_set_starttext', icon_custom_emoji_id='5395444784611480792')
    kb.button(text='Set Welcome Banner', callback_data='admin_set_banner', icon_custom_emoji_id='5409029744693897259')
    kb.button(text='Back', callback_data='back_to_start', icon_custom_emoji_id='5411225014148014586')
    kb.adjust(2, 2, 1, 1)
    if isinstance(event, Message):
        await event.answer(panel_text, reply_markup=kb.as_markup())
    elif isinstance(event, CallbackQuery):
        await event.answer()
        try:
            if event.message.photo:
                await event.message.edit_caption(caption=panel_text, reply_markup=kb.as_markup())
            else:
                await event.message.edit_text(panel_text, reply_markup=kb.as_markup())
        except Exception:
            await event.message.delete()
            await event.message.answer(panel_text, reply_markup=kb.as_markup())

@router.callback_query(F.data == 'admin_set_upi')
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def admin_set_upi_prompt(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Cancel', callback_data='admin_settings_menu')
    await call.message.answer("<tg-emoji emoji-id='5409048419211682843'>💳</tg-emoji> <b>Send the new UPI ID</b> (e.g. <code>devanshsingh2@fam</code>):", reply_markup=kb.as_markup())
    await state.set_state(AdminSettings.waiting_for_upi)
    await call.answer()

@router.message(AdminSettings.waiting_for_upi)
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def admin_process_upi(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    new_upi = message.text.strip()
    await membership_settings_col.update_one({'type': 'qr'}, {'$set': {'upi_id': new_upi, 'file_id': None}}, upsert=True)
    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text='⚙️️ Return to Admin Settings', callback_data='admin_settings_menu')
    await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>UPI ID updated to:</b> <code>{new_upi}</code>\nDynamic QR codes will now generate with this UPI ID.", reply_markup=kb.as_markup())

@router.callback_query(F.data == 'admin_set_qr')
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def admin_set_qr_prompt(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Cancel', callback_data='admin_settings_menu')
    await call.message.answer("<tg-emoji emoji-id='5427168083074628963'>📸</tg-emoji> <b>Send the new QR Code photo now:</b>", reply_markup=kb.as_markup())
    await state.set_state(AdminSettings.waiting_for_qr_photo)
    await call.answer()

@router.message(AdminSettings.waiting_for_qr_photo, F.photo)
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def admin_process_qr_photo(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    file_id = message.photo[-1].file_id
    await membership_settings_col.update_one({'type': 'qr'}, {'$set': {'file_id': file_id}}, upsert=True)
    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text='⚙️️ Return to Admin Settings', callback_data='admin_settings_menu')
    await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Custom QR Code Photo saved!</b>", reply_markup=kb.as_markup())

@router.callback_query(F.data == 'admin_reset_dynamic_qr')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def admin_reset_dynamic_qr(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    await membership_settings_col.update_one({'type': 'qr'}, {'$set': {'file_id': None}}, upsert=True)
    await call.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> Switched back to Dynamic UPI QR codes!", show_alert=True)
    await show_admin_settings(call, state)

@router.callback_query(F.data == 'admin_set_prices')
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def admin_set_prices_prompt(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Cancel', callback_data='admin_settings_menu')
    await call.message.answer("<tg-emoji emoji-id='5409048419211682843'>💰</tg-emoji> <b>Send the Membership Plans & Prices:</b>\n\nFormat: <code>7D 49 15D 89 30D 149</code>\n(DayCount Price DayCount Price...)", reply_markup=kb.as_markup())
    await state.set_state(AdminSettings.waiting_for_prices)
    await call.answer()

@router.message(AdminSettings.waiting_for_prices)
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def admin_process_prices(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    args = message.text.split()
    if not args or len(args) % 2 != 0:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Invalid format. Example: <code>7D 49 15D 89 30D 149</code>")
        return
    plans = []
    try:
        for i in range(0, len(args), 2):
            label = args[i].upper()
            price = args[i + 1]
            days = int(label.replace('D', ''))
            plans.append({'label': label, 'days': days, 'price': price})
        await membership_settings_col.update_one({'type': 'plans'}, {'$set': {'plans': plans}}, upsert=True)
        await state.clear()
        kb = InlineKeyboardBuilder()
        kb.button(text='⚙️️ Return to Admin Settings', callback_data='admin_settings_menu')
        await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Membership Plans & Prices updated successfully!</b>", reply_markup=kb.as_markup())
    except ValueError:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Error: Days and Prices must be numbers (e.g. 7D 49).")

@router.callback_query(F.data == 'admin_set_memtext')
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def admin_set_memtext_prompt(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    kb = InlineKeyboardBuilder()
    kb.button(text='🔄 Reset to Default', callback_data='admin_reset_memtext')
    kb.button(text='🔙 Cancel', callback_data='admin_settings_menu')
    kb.adjust(1)
    await call.message.answer("<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> <b>Send the new VIP Membership screen text:</b>\n\n• Include <code>{status}</code> where the Active/Inactive badge should be.\n• All custom emojis, bold, italics, links, and blockquotes will be saved!", reply_markup=kb.as_markup())
    await state.set_state(AdminSettings.waiting_for_mem_text)
    await call.answer()

@router.callback_query(F.data == 'admin_reset_memtext')
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def admin_reset_memtext(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    await membership_settings_col.delete_one({'type': 'ui_text'})
    await state.clear()
    await call.answer("<tg-emoji emoji-id='5375338737028841420'>🔄</tg-emoji> Membership text reset to default design!", show_alert=True)
    await show_admin_settings(call, state)

@router.message(AdminSettings.waiting_for_mem_text)
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def admin_process_memtext(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    custom_html = message.html_text
    await membership_settings_col.update_one({'type': 'ui_text'}, {'$set': {'membership_msg': custom_html}}, upsert=True)
    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text='⚙️️ Return to Admin Settings', callback_data='admin_settings_menu')
    await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>VIP Membership screen text updated!</b>", reply_markup=kb.as_markup())

@router.callback_query(F.data == 'admin_set_starttext')
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def admin_set_starttext_prompt(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    kb = InlineKeyboardBuilder()
    kb.button(text='🔄 Reset to Default', callback_data='admin_reset_starttext')
    kb.button(text='🔙 Cancel', callback_data='admin_settings_menu')
    kb.adjust(1)
    await call.message.answer("<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Send the new Welcome / Start Message:</b>\n\nAll formatting, bold, italics, links, and styling will be preserved!", reply_markup=kb.as_markup())
    await state.set_state(AdminSettings.waiting_for_start_text)
    await call.answer()

@router.callback_query(F.data == 'admin_reset_starttext')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def admin_reset_starttext(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    await start_settings_col.delete_one({'type': 'start_msg'})
    await state.clear()
    await call.answer("<tg-emoji emoji-id='5375338737028841420'>🔄</tg-emoji> Welcome message reset to default design!", show_alert=True)
    await show_admin_settings(call, state)

@router.message(AdminSettings.waiting_for_start_text)
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def admin_process_starttext(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    new_text = message.html_text
    await start_settings_col.update_one({'type': 'start_msg'}, {'$set': {'text': new_text}}, upsert=True)
    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text='⚙️️ Return to Admin Settings', callback_data='admin_settings_menu')
    await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Welcome message updated!</b>", reply_markup=kb.as_markup())

@router.callback_query(F.data == 'admin_set_banner')
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def admin_set_banner_prompt(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        return
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Cancel', callback_data='admin_settings_menu')
    await call.message.answer("<tg-emoji emoji-id='5409029744693897259'>🖼</tg-emoji> <b>Send the new Welcome Banner Photo:</b>", reply_markup=kb.as_markup())
    await state.set_state(AdminSettings.waiting_for_banner_photo)
    await call.answer()

@router.message(AdminSettings.waiting_for_banner_photo, F.photo)
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def admin_process_banner_photo(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    global _cached_welcome_file_id
    _cached_welcome_file_id = message.photo[-1].file_id
    try:
        file = await bot.get_file(_cached_welcome_file_id)
        await bot.download_file(file.file_path, WELCOME_IMAGE_PATH)
    except Exception as e:
        logger.error(f'Error downloading new welcome image: {e}')
    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text='⚙️️ Return to Admin Settings', callback_data='admin_settings_menu')
    await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Welcome Banner Photo updated!</b>", reply_markup=kb.as_markup())

@router.message(Command('setmemtext'))
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def set_membership_text(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    if not message.reply_to_message:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> <b>How to use:</b>\n1. Write a message with the exact formatting (Bold, Italic, Emojis) you want.\n2. Include <code>{status}</code> where you want the Active/Inactive info to appear.\n3. <b>Reply</b> to that message with <code>/setmemtext</code>.")
        return
    custom_html = message.reply_to_message.html_text
    await membership_settings_col.update_one({'type': 'ui_text'}, {'$set': {'membership_msg': custom_html}}, upsert=True)
    response_text = "<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Membership text updated!</b>"
    if '{status}' not in custom_html:
        response_text += "\n\n<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> <b>Note:</b> You didn't include <code>{status}</code> in your text. The user's active/expired status will NOT be visible."
    await message.answer(response_text)

@router.message(Command('membership'))
# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'membership')
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def cmd_membership(event: Union[Message, CallbackQuery]):
    user_id = event.from_user.id
    user_mem = await get_membership(user_id)
    status_text = "<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Inactive</b>"
    kb = InlineKeyboardBuilder()
    if user_mem:
        expiry = user_mem['membership_expiry']
        if expiry.tzinfo is None:
            expiry = IST.localize(expiry)
        now_ist = datetime.now(IST)
        if expiry > now_ist:
            expiry_str = expiry.strftime('%d-%b-%Y %I:%M %p IST')
            days_left = (expiry - now_ist).days
            status_text = f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Active</b>\n<tg-emoji emoji-id='5395444784611480792'>📅</tg-emoji> Expires: {expiry_str}\n<tg-emoji emoji-id='5375338737028841420'>⏳</tg-emoji> Remaining: {days_left} days"
            if days_left >= 28:
                kb.button(text='Set Global Channel', callback_data='set_user_global_sub', icon_custom_emoji_id='5424818078833715060')
        else:
            status_text = "<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>Expired</b>"
    ui_settings = await membership_settings_col.find_one({'type': 'ui_text'})
    default_template = f"<tg-emoji emoji-id='5438496463044752972'>⭐️</tg-emoji> <b>MEMBERSHIP-</b> {{status}}\n\n<tg-emoji emoji-id='6336811288437460963'>💜</tg-emoji> <u><b>PREMIUM FEATURES</b></u> <tg-emoji emoji-id='6082358798549257477'>🥶</tg-emoji>\n  ✦ ━━━━━━━━━━━━ ✦\n<blockquote>• <tg-emoji emoji-id='6336648809824655471'>🐈\u200d⬛</tg-emoji> <b>Add your own custom thumbnail / vote post image</b></blockquote>\n<blockquote>• <tg-emoji emoji-id='6339054897748511636'>🐈\u200d⬛</tg-emoji> <b>Auto vote deduction if a user leaves after voting during giveaways</b> <tg-emoji emoji-id='5424972470023104089'>🔥</tg-emoji> (Free for Sometime)</blockquote>\n<blockquote>• <tg-emoji emoji-id='6080258529476742663'>🐈\u200d⬛</tg-emoji> <b>Add 1 extra Force-Join channel/group before voting</b> <tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji></blockquote>\n<blockquote>• <tg-emoji emoji-id='6336648809824655471'>🐈\u200d⬛</tg-emoji> <b>Set 1 main Force-Join for all bot users</b>\n\n<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <i>(Available only with minimum 1-week membership <tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji>)</i></blockquote>\n  ✦ ━━━━━━━━━━━━ ✦\n<tg-emoji emoji-id='5217822164362739968'>👑</tg-emoji> <b>Upgrade to unlock <tg-emoji emoji-id='5424972470023104089'>🔥</tg-emoji> full control &amp; <tg-emoji emoji-id='5427168083074628963'>🚀</tg-emoji> maximum reach <tg-emoji emoji-id='5312369268019444105'>💀</tg-emoji></b>\n\n{BRAND_FOOTER}"
    if ui_settings and ui_settings.get('membership_msg'):
        template = ui_settings['membership_msg']
    else:
        template = default_template
    final_text = template.replace('{status}', status_text)
    DEFAULT_PLANS = [{'label': '7 Days', 'days': 7, 'price': '49'}, {'label': '15 Days', 'days': 15, 'price': '89'}, {'label': '30 Days', 'days': 30, 'price': '149'}]
    settings = await membership_settings_col.find_one({'type': 'plans'})
    plans = settings.get('plans') if settings and settings.get('plans') else DEFAULT_PLANS
    for plan in plans:
        kb.button(text=f"{plan['label']} - ₹{plan['price']}", callback_data=f"buy_mem_{plan['days']}_{plan['price']}", icon_custom_emoji_id='5427168083074628963')
    kb.button(text='Developer (Aryan)', url='https://t.me/thatonearyan', icon_custom_emoji_id='5269617636001460986')
    kb.button(text='Back', callback_data='back_to_start', icon_custom_emoji_id='5411225014148014586')
    kb.adjust(1)
    if isinstance(event, Message):
        await event.answer(final_text, reply_markup=kb.as_markup())
    elif isinstance(event, CallbackQuery):
        await event.answer()
        if event.message.photo:
            try:
                await event.message.edit_caption(caption=final_text, reply_markup=kb.as_markup())
            except Exception:
                await event.message.delete()
                await event.message.answer(final_text, reply_markup=kb.as_markup())
        else:
            await event.message.edit_text(final_text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('buy_mem_'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def buy_mem_start(call: CallbackQuery, state: FSMContext):
    days = int(call.data.split('_')[2])
    price = call.data.split('_')[3]
    qr_data = await membership_settings_col.find_one({'type': 'qr'})
    upi_id = qr_data.get('upi_id', 'devanshsingh2@fam') if qr_data else 'devanshsingh2@fam'
    await state.update_data(plan_days=days, plan_price=price, upi_id=upi_id)
    kb = InlineKeyboardBuilder()
    kb.button(text="I've Paid", callback_data='mem_paid_confirm', icon_custom_emoji_id='6339289076545358952')
    kb.button(text='Cancel', callback_data='delete_msg', icon_custom_emoji_id='6053019808230805244')
    kb.adjust(1)
    caption_text = f"<tg-emoji emoji-id='5409048419211682843'>💳</tg-emoji> <b>Purchase {days} Days VIP Membership</b>\n\n<tg-emoji emoji-id='5424972470023104089'>💸</tg-emoji> Amount: <b>₹{price}</b>\n<tg-emoji emoji-id='5427168083074628963'>🆔</tg-emoji> UPI ID: <code>{upi_id}</code> (tap to copy)\n\n<i>Scan the QR code above or pay to the UPI ID, then tap 'I\\'ve Paid' to submit your screenshot.</i>"
    if qr_data and qr_data.get('file_id'):
        await call.message.answer_photo(photo=qr_data['file_id'], caption=caption_text, reply_markup=kb.as_markup())
    else:
        qr_bytes = generate_upi_qr(upi_id=upi_id, amount=str(price), note=f'VIP_{days}D')
        qr_file = BufferedInputFile(qr_bytes, filename='payment_qr.png')
        await call.message.answer_photo(photo=qr_file, caption=caption_text, reply_markup=kb.as_markup())
    await state.set_state(BuyMembership.waiting_for_proof)
    await call.answer()

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'mem_paid_confirm', BuyMembership.waiting_for_proof)
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def mem_ask_proof(call: CallbackQuery):
    await call.message.edit_caption(caption="<tg-emoji emoji-id='5427168083074628963'>📸</tg-emoji> <b>Upload Screenshot</b>\n\nPlease send the transaction screenshot now.")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(BuyMembership.waiting_for_proof)
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def mem_process_proof(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Please send an image.")
        return
    data = await state.get_data()
    days = data['plan_days']
    kb = InlineKeyboardBuilder()
    kb.button(text='Approve', callback_data=f'aprmem_{message.from_user.id}_{days}', icon_custom_emoji_id='6339289076545358952')
    kb.button(text='Reject', callback_data=f'rejmem_{message.from_user.id}', icon_custom_emoji_id='6053019808230805244')
    kb.adjust(2)
    caption = f"<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> <b>New Membership Purchase</b>\n\n<tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> User: {message.from_user.mention_html()}\n<tg-emoji emoji-id='5427168083074628963'>🆔</tg-emoji> ID: <code>{message.from_user.id}</code>\n<tg-emoji emoji-id='5395444784611480792'>📅</tg-emoji> Plan: {days} Days\n<tg-emoji emoji-id='5409048419211682843'>💸</tg-emoji> Price: ₹{data['plan_price']}"
    for admin in OWNER_IDS:
        try:
            await bot.send_photo(chat_id=admin, photo=message.photo[-1].file_id, caption=caption, reply_markup=kb.as_markup())
        except:
            pass
    await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Proof Sent!</b> Waiting for admin approval.")
    await state.clear()

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('aprmem_'))
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def approve_membership(call: CallbackQuery):
    _, user_id_str, days_str = call.data.split('_')
    user_id = int(user_id_str)
    days = int(days_str)
    current_mem = await get_membership(user_id)
    now = datetime.now(IST)
    if current_mem:
        new_expiry = current_mem['membership_expiry'] + timedelta(days=days)
        msg_type = 'extended'
    else:
        new_expiry = now + timedelta(days=days)
        msg_type = 'activated'
    await users_col.update_one({'user_id': user_id}, {'$set': {'membership_expiry': new_expiry, 'membership_level': 'premium'}}, upsert=True)
    date_fmt = new_expiry.strftime('%d-%b-%Y %I:%M %p IST')
    try:
        await bot.send_message(user_id, f"<tg-emoji emoji-id='5461151367559141950'>🎉</tg-emoji> <b>Payment Approved!</b>\n\n<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> {days} Days Membership {msg_type}.\n<tg-emoji emoji-id='5395444784611480792'>📅</tg-emoji> <b>Valid till:</b> {date_fmt}\n\n<i>Type /membership to manage.</i>")
    except:
        pass
    log_text = f"<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> <b>Membership Active</b>\nUser: <a href='tg://user?id={user_id}'>{user_id}</a>\nPlan: {days} Days\nEnds: {date_fmt}<b>Features </b>:"
    try:
        await bot.send_message(LOG_CHANNEL_ID, log_text)
    except:
        pass
    await call.message.edit_caption(caption=call.message.caption + "\n\n<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>APPROVED</b>")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('rejmem_'))
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def reject_membership(call: CallbackQuery):
    user_id = int(call.data.split('_')[1])
    try:
        await bot.send_message(user_id, "<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Your membership request was rejected.")
    except:
        pass
    await call.message.edit_caption(caption=call.message.caption + "\n\n<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>REJECTED</b>")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('gift'))
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def cmd_gift(message: Message, state: FSMContext):
    if message.from_user.id not in OWNER_IDS:
        return
    await message.answer("<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <b>Gift Membership</b>\n\nSend the User ID.")
    await state.set_state(AdminGift.waiting_for_user)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(AdminGift.waiting_for_user)
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def gift_get_user(message: Message, state: FSMContext):
    try:
        uid = int(message.text.strip())
        await state.update_data(target_id=uid)
        kb = InlineKeyboardBuilder()
        kb.button(text='1 Day', callback_data='gift_1')
        kb.button(text='7 Days', callback_data='gift_7')
        kb.button(text='30 Days', callback_data='gift_30')
        await message.answer("<tg-emoji emoji-id='5375338737028841420'>⏳</tg-emoji> <b>Select Duration</b>", reply_markup=kb.as_markup())
    except:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid ID.")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('gift_'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def gift_confirm(call: CallbackQuery, state: FSMContext):
    days = int(call.data.split('_')[1])
    data = await state.get_data()
    user_id = data['target_id']
    now = datetime.now(IST)
    new_expiry = now + timedelta(days=days)
    current = await get_membership(user_id)
    if current:
        new_expiry = current['membership_expiry'] + timedelta(days=days)
    await users_col.update_one({'user_id': user_id}, {'$set': {'membership_expiry': new_expiry}}, upsert=True)
    await call.message.edit_text(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> Gifted {days} days to <code>{user_id}</code>")
    try:
        await bot.send_message(user_id, f"<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <b>You received a gift!</b>\n\n<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> {days} Days Membership added by Admin.")
    except:
        pass
    await state.clear()

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('conmembership'))
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def cmd_conmembership(message: Message):
    if message.from_user.id not in OWNER_IDS:
        return
    now = datetime.now(IST)
    cursor = users_col.find({'membership_expiry': {'$gt': now}})
    members = await cursor.to_list(None)
    if not members:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> No active memberships.")
        return
    text = "<tg-emoji emoji-id='5427168083074628963'>💎</tg-emoji> <b>Active Memberships</b>\n\n"
    kb = InlineKeyboardBuilder()
    for m in members:
        expiry = m['membership_expiry'].strftime('%d-%b')
        name = m.get('first_name', 'User')
        btn_text = f'{name} ({expiry})'
        kb.button(text=btn_text, callback_data=f"view_mem_{m['user_id']}")
    kb.adjust(1)
    await message.answer(text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('view_mem_'))
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def view_member_details(call: CallbackQuery):
    user_id = int(call.data.split('_')[2])
    user = await users_col.find_one({'user_id': user_id})
    if not user:
        await call.answer('User not found', show_alert=True)
        return
    expiry = user.get('membership_expiry')
    if not expiry:
        text = "<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Membership Expired."
    else:
        text = f"<tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> <b>User Details</b>\nID: <code>{user_id}</code>\nName: {user.get('first_name')}\n<tg-emoji emoji-id='5395444784611480792'>📅</tg-emoji> Expires: {expiry.strftime('%d-%b-%Y %H:%M')}\n"
    kb = InlineKeyboardBuilder()
    kb.button(text='🚫 Cancel Membership', callback_data=f'cancel_mem_{user_id}')
    kb.button(text='🔙 Back', callback_data='delete_msg')
    await call.message.edit_text(text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('cancel_mem_'))
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def cancel_membership(call: CallbackQuery):
    user_id = int(call.data.split('_')[2])
    await users_col.update_one({'user_id': user_id}, {'$unset': {'membership_expiry': ''}})
    await call.message.edit_text("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> Membership Cancelled.")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'set_user_global_sub')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def start_set_user_global(call: CallbackQuery, state: FSMContext):
    mem = await get_membership(call.from_user.id)
    if not mem:
        await call.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Membership expired", show_alert=True)
        return
    await call.message.answer("<tg-emoji emoji-id='5217822164362739968'>👑</tg-emoji> <b>Set Global Force-Join Channel</b>\n\nSend Channel ID and Link.\nFormat: <code>-100xxxxx https://t.me/...</code>\n\n<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> Bot must be Admin there!\nℹ️ Replaces any previous channel set by you.")
    await state.set_state(SetUserGlobal.waiting_for_input)
    await call.answer()

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(SetUserGlobal.waiting_for_input)
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def process_user_global(message: Message, state: FSMContext):
    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            raise ValueError
        ch_id = int(parts[0])
        link = parts[1]
        try:
            m = await bot.get_chat_member(ch_id, bot.id)
            if m.status != ChatMemberStatus.ADMINISTRATOR:
                await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Bot is not admin in that channel.")
                return
        except:
            await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Can't access channel. Make sure ID is correct and I am added.")
            return
        doc = {'user_id': message.from_user.id, 'channel': {'id': ch_id, 'link': link, 'title': 'Sponsored Channel'}}
        await user_global_channels_col.update_one({'user_id': message.from_user.id}, {'$set': doc}, upsert=True)
        await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Global Channel Set!</b>\nIt will be active as long as your membership is valid.")
        await state.clear()
    except:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid format. Use: <code>ID LINK</code>")

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('vote_'))
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def handle_channel_vote(call: CallbackQuery):
    """
    Handles voting logic for organic giveaways.
    Enforces STRICT single vote per giveaway policy.
    Format: vote_{participant_id}_{ga_id}
    """
    try:
        parts = call.data.split('_')
        if len(parts) < 3:
            raise ValueError
        participant_id_str, ga_id = (parts[1], parts[2])
        participant_id = int(participant_id_str)
    except (ValueError, IndexError):
        await call.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid vote data structure.", show_alert=True)
        return
    voter = call.from_user
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if not ga or ga.get('status') != 'active':
        await call.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> This Giveaway has ended or is inactive.", show_alert=True)
        return
    if voter.id == participant_id:
        await call.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> ᴏᴘᴇʀᴀᴛɪᴏɴ ᴅᴇɴɪᴇᴅ\n\nʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴠᴏᴛᴇ ғᴏʀ ʏᴏᴜʀsᴇʟғ!", show_alert=True)
        return
    existing_vote = await votes_col.find_one({'ga_id': ga_id, 'voter_id': voter.id})
    if existing_vote:
        if existing_vote['participant_id'] == participant_id:
            msg = "<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴠᴏᴛᴇᴅ ғᴏʀ ᴛʜɪs ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ."
        else:
            msg = "<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> ᴠᴏᴛᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ\n\n🚫 ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴠᴏᴛᴇ ғᴏʀ ᴏɴᴇ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ɪɴ ᴛʜɪs ɢɪᴠᴇᴀᴡᴀʏ.\nʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴠᴏᴛᴇ."
        await call.answer(msg, show_alert=True)
        return
    participant = await participants_col.find_one({'ga_id': ga_id, 'user_id': participant_id})
    if not participant:
        await call.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Error: Participant record not found.", show_alert=True)
        return
    missing = await get_missing_channels(voter.id, ga)
    if missing:
        channel_names = '\n'.join([f"• {ch.get('title', 'Required Channel')}" for ch in missing])
        alert_msg = f'🚫 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ\n\nʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴛʜᴇ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs ʙᴇғᴏʀᴇ ᴠᴏᴛɪɴɢ:\n{channel_names}\n\n👉 ᴜsᴇ ᴛʜᴇ ᴊᴏɪɴ ʙᴜᴛᴛᴏɴs ᴀʙᴏᴠᴇ ᴛʜɪs ᴘᴏsᴛ!'
        await call.answer(alert_msg, show_alert=True)
        return
    await votes_col.insert_one({'ga_id': ga_id, 'voter_id': voter.id, 'participant_id': participant_id, 'voted_at': datetime.now()})
    await participants_col.update_one({'_id': participant['_id']}, {'$inc': {'vote_count': 1}})
    new_count = participant.get('vote_count', 0) + 1
    chan_kb = InlineKeyboardBuilder()
    extras = ga.get('extra_channel') or ga.get('extra_channels')
    if extras:
        if isinstance(extras, dict):
            extras = [extras]
        for ch in extras:
            chan_kb.button(text='📢 Join', url=ch['link'])
    chan_kb.button(text=f"<tg-emoji emoji-id='5409029744693897259'>🗳</tg-emoji> Vote ({new_count})", callback_data=call.data)
    chan_kb.adjust(1)
    try:
        await call.message.edit_reply_markup(reply_markup=chan_kb.as_markup())
    except TelegramBadRequest:
        pass
    except Exception as e:
        print(f'Error updating markup: {e}')
    alert_text = f"[<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji>] ᴠᴏᴛᴇ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\n\n‣ ᴠᴏᴛᴇ ғʀᴏᴍ : {voter.full_name}\n‣ ɴᴇᴡ ᴄᴏᴜɴᴛ : {new_count}\n‣ ᴠᴏᴛᴇᴅ ғᴏʀ : {participant.get('name', 'Participant')}\n‣ ʙᴏᴛ : @{BOTUSER}\n‣ ᴅᴇᴠ : @thatonearyan"
    await call.answer(alert_text, show_alert=True)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('buy_start_'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def buy_start(call: CallbackQuery, state: FSMContext):
    ga_id = call.data.split('_')[2]
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    if ga['status'] != 'active':
        await call.answer('Giveaway ended.', show_alert=True)
        return
    methods = []
    if ga.get('currency_type') in ['curr_inr', 'curr_both']:
        methods.append('inr')
    if ga.get('currency_type') in ['curr_star', 'curr_both']:
        methods.append('star')
    await state.update_data(ga_id=ga_id, ga_doc=ga)
    if len(methods) > 1:
        kb = InlineKeyboardBuilder()
        kb.button(text='🇮🇳 INR (QR)', callback_data='pay_method_inr')
        kb.adjust(1)
        kb.button(text='⭐️ Stars', callback_data='pay_method_star')
        await call.message.answer("<tg-emoji emoji-id='5409048419211682843'>💳</tg-emoji> <b>Select Payment Method:</b>", reply_markup=kb.as_markup())
        await state.set_state(BuyVotes.waiting_for_method)
    else:
        await process_payment_display(call.message, state, methods[0])
    await call.answer()

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(BuyVotes.waiting_for_method)
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def payment_method_selected(call: CallbackQuery, state: FSMContext):
    method = call.data.split('_')[2]
    await process_payment_display(call.message, state, method)

# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def process_payment_display(message: Message, state: FSMContext, method: str):
    data = await state.get_data()
    ga = data['ga_doc']
    rates = ga['rates']
    await state.update_data(selected_method=method)
    info_text = ''
    if method == 'inr':
        rate = rates.get('inr')
        info_text = f'🇮🇳 <b>Pay via QR</b>\n\nRate: <b>{rate} Votes / 1 INR</b>\n\n1. Scan QR below.\n2. Pay desired amount.\n3. Send Screenshot here.'
        if ga.get('qr_code'):
            await message.answer_photo(photo=ga['qr_code'], caption=info_text)
        else:
            await message.answer(info_text)
    else:
        rate = rates.get('star')
        target_user = ga.get('star_user')
        info_text = f"<tg-emoji emoji-id='5438496463044752972'><tg-emoji emoji-id='5438496463044752972'>⭐</tg-emoji>️</tg-emoji> <b>Pay via Stars</b>\n\nRate: <b>{rate} Votes / 1 Star</b>\n\n1. Send stars to {target_user}.\n2. Send Screenshot of transaction here."
        await message.answer(info_text)
    await state.set_state(BuyVotes.waiting_for_proof)

@router.message(BuyVotes.waiting_for_proof)
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def receive_proof(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Please send a screenshot image.")
        return
    data = await state.get_data()
    ga = data['ga_doc']
    method = data['selected_method']
    await state.update_data(proof_file_id=message.photo[-1].file_id)
    curr_name = 'INR' if method == 'inr' else 'Stars'
    await message.answer(f'🔢 <b>Enter Amount Paid ({curr_name})</b>\n\nJust type the number (e.g. 50).')
    await state.set_state(BuyVotes.waiting_for_amount)

@router.message(BuyVotes.waiting_for_amount)
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def receive_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text.strip())
    except:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid number. Try again.")
        return
    data = await state.get_data()
    ga = data['ga_doc']
    method = data['selected_method']
    rate = ga['rates'][method]
    votes_to_add = amount * rate
    txn_id = generate_id(6)
    txn = {'txn_id': txn_id, 'ga_id': ga['ga_id'], 'user_id': message.from_user.id, 'amount': amount, 'method': method, 'votes_to_add': votes_to_add, 'proof': data['proof_file_id'], 'status': 'pending', 'timestamp': datetime.now()}
    await transactions_col.insert_one(txn)
    kb = InlineKeyboardBuilder()
    kb.button(text='Approve', callback_data=f'appr_yes_{txn_id}', icon_custom_emoji_id='6339289076545358952')
    kb.button(text='Reject', callback_data=f'appr_no_{txn_id}', icon_custom_emoji_id='6053019808230805244')
    kb.adjust(2)
    caption = f"<tg-emoji emoji-id='5409048419211682843'>💰</tg-emoji> <b>New Paid Vote Request</b>\nUser: {message.from_user.mention_html()}\nMethod: {method.upper()}\nAmount: {amount}\nVotes: {votes_to_add}\nProof attached above."
    try:
        await bot.send_photo(chat_id=ga['creator_id'], photo=data['proof_file_id'], caption=caption, reply_markup=kb.as_markup())
        await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Proof Sent!</b> Waiting for admin approval.")
    except Exception as e:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Failed to contact admin. Try again later.")
    await state.clear()

@router.callback_query(F.data.startswith('appr_'))
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def handle_approval(call: CallbackQuery):
    action, txn_id = (call.data.split('_')[1], call.data.split('_')[2])
    txn = await transactions_col.find_one({'txn_id': txn_id})
    if not txn or txn['status'] != 'pending':
        await call.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Already processed.", show_alert=True)
        return
    if action == 'no':
        await transactions_col.update_one({'txn_id': txn_id}, {'$set': {'status': 'rejected'}})
        await call.message.edit_caption(caption=call.message.caption + "\n\n<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>REJECTED</b>")
        await bot.send_message(txn['user_id'], "<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Your paid vote request was rejected.")
    else:
        await transactions_col.update_one({'txn_id': txn_id}, {'$set': {'status': 'approved'}})
        await participants_col.update_one({'ga_id': txn['ga_id'], 'user_id': txn['user_id']}, {'$inc': {'vote_count': txn['votes_to_add'], 'paid_votes_count': txn['votes_to_add']}})
        p = await participants_col.find_one({'ga_id': txn['ga_id'], 'user_id': txn['user_id']})
        ga = await giveaways_col.find_one({'ga_id': txn['ga_id']})
        new_count = p['vote_count']
        kb = InlineKeyboardBuilder()
        kb.button(text=f"<tg-emoji emoji-id='5409029744693897259'>🗳</tg-emoji> Vote ({new_count})", callback_data=f"vote_{p['user_id']}_{ga['ga_id']}")
        kb.adjust(1)
        try:
            await bot.edit_message_reply_markup(chat_id=p['channel_id'], message_id=p['msg_id'], reply_markup=kb.as_markup())
        except:
            pass
        await call.message.edit_caption(caption=call.message.caption + "\n\n<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>APPROVED</b>")
        succ_msg = f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Payment Approved!</b>\n+{txn['votes_to_add']} Votes added.\nCurrent Total: {new_count}"
        await bot.send_message(txn['user_id'], succ_msg)
        try:
            await bot.send_message(ga['target_channel_id'], f"🚀 <b>PAID VOTES!</b>\n<blockquote>🧘\u200d♂️USER :{p['name']}</blockquote>\n<blockquote><tg-emoji emoji-id='5409048419211682843'>💳</tg-emoji> Purchased : {txn['votes_to_add']} votes!</blockquote>")
        except:
            pass

@router.message(Command('stats'))
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def cmd_stats(message: Message):
    if message.from_user.id not in OWNER_IDS:
        return
    total_users = await users_col.count_documents({})
    total_gas = await giveaways_col.count_documents({})
    active_gas = await giveaways_col.count_documents({'status': 'active'})
    text = f"<tg-emoji emoji-id='5409029744693897259'>📊</tg-emoji> <b>ʙɪᴛᴢ ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ</b>\n\n<tg-emoji emoji-id='5269617636001460986'>👥</tg-emoji> <b>Total Users:</b> {total_users}\n<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <b>Total Giveaways:</b> {total_gas}\n<tg-emoji emoji-id='6339289076545358952'>🟢</tg-emoji> <b>Active Giveaways:</b> {active_gas}\n\n{POWERED_BY_TEXT}"
    kb = InlineKeyboardBuilder()
    kb.button(text='🏆 Top Creators', callback_data='admin_top_users')
    kb.button(text='👨‍💻 Developer (Aryan)', url='https://t.me/thatonearyan', icon_custom_emoji_id='5269617636001460986')
    kb.adjust(1, 1)
    await message.answer(text, reply_markup=kb.as_markup())

@router.callback_query(F.data == 'admin_top_users')
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def show_top_creators(call: CallbackQuery):
    if call.from_user.id not in OWNER_IDS:
        return
    pipeline = [{'$group': {'_id': '$creator_id', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 10}]
    results = await giveaways_col.aggregate(pipeline).to_list(None)
    text = "<tg-emoji emoji-id='5204046146955153467'>🏆</tg-emoji> <b>Top Giveaway Creators</b>\n\n"
    if not results:
        text += 'No data found.'
    else:
        for idx, item in enumerate(results, 1):
            user_id = item['_id']
            count = item['count']
            user_doc = await users_col.find_one({'user_id': user_id})
            name = user_doc['first_name'] if user_doc else 'Unknown'
            text += f'{idx}. {name} (<code>{user_id}</code>) - <b>{count} GAs</b>\n'
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Back', callback_data='delete_msg')
    try:
        await call.message.edit_text(text, reply_markup=kb.as_markup())
    except Exception:
        await call.answer()

@router.callback_query(F.data == 'delete_msg')
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def delete_msg(call: CallbackQuery):
    await call.message.delete()

@router.message(Command('setjoin'))
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def cmd_setjoin(message: Message, state: FSMContext):
    if message.from_user.id not in OWNER_IDS:
        return
    settings = await settings_col.find_one({'type': 'force_join'})
    current_channels = settings.get('channels', []) if settings else []
    text = f"<tg-emoji emoji-id='5251203410396458957'>🛡</tg-emoji> <b>Force Join Settings</b>\nCurrent Channels: {len(current_channels)}/10\n\n"
    for i, ch in enumerate(current_channels, 1):
        text += f"{i}. ID: <code>{ch['id']}</code>\n"
    kb = InlineKeyboardBuilder()
    if len(current_channels) < 10:
        kb.button(text='➕ Add Channel', callback_data='add_fsub')
    kb.button(text='🗑 Clear All', callback_data='clear_fsub')
    kb.button(text='❌ Close', callback_data='delete_msg')
    kb.adjust(1)
    await message.answer(text, reply_markup=kb.as_markup())

@router.callback_query(F.data == 'clear_fsub')
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def clear_fsub(call: CallbackQuery):
    if call.from_user.id not in OWNER_IDS:
        return
    await settings_col.update_one({'type': 'force_join'}, {'$set': {'channels': []}}, upsert=True)
    await call.answer('All channels removed!', show_alert=True)
    await call.message.delete()

@router.callback_query(F.data == 'add_fsub')
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def start_add_fsub(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in OWNER_IDS:
        return
    await call.message.answer("<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Add Must-Join Channel</b>\n\nSend the <b>Channel ID</b> and <b>Invite Link</b> separated by a space.\nExample:\n<code>-1001234567890 https://t.me/+AbCdEfG</code>\n\n<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> <i>Make sure the Bot is Admin in that channel!</i>")
    await state.set_state(SetJoin.waiting_for_input)
    await call.answer()

@router.message(SetJoin.waiting_for_input)
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def process_fsub_input(message: Message, state: FSMContext):
    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid format. Use: <code>ID LINK</code>")
            return
        ch_id = int(parts[0])
        link = parts[1]
        try:
            member = await bot.get_chat_member(chat_id=ch_id, user_id=bot.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> I am not an admin in that channel! Promote me first.")
                return
        except Exception as e:
            await message.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Could not access channel: {e}")
            return
        await settings_col.update_one({'type': 'force_join'}, {'$push': {'channels': {'id': ch_id, 'link': link}}}, upsert=True)
        await message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Channel Added to Force Subscription!</b>")
        await state.clear()
    except ValueError:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> ID must be a number.")

@router.message(Command('support'))
# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('about'))
@router.message(Command('help'))
# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('developer'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def cmd_support(message: Message):
    text = f"<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <b>{BRAND_NAME_SMALLCAPS} ꜱᴜᴘᴘᴏʀᴛ &amp; ᴄᴏɴᴛᴀᴄᴛ</b>\n\n<blockquote><tg-emoji emoji-id='6336811288437460963'>❤️</tg-emoji> <b>ᴀᴅᴍɪɴ:</b> <a href='{SUPPORT_URL}'>{SUPPORT_NAME}</a> (<code>@{SUPPORT_USERNAME}</code>)\n<tg-emoji emoji-id='5949775417274536507'>⚡️</tg-emoji> <b>ᴄʜᴀɴɴᴇʟ:</b> <a href='{NETWORK_URL}'>{NETWORK_NAME}</a> (<code>@{NETWORK_USERNAME}</code>)\n<tg-emoji emoji-id='5269617636001460986'>👨\u200d💻</tg-emoji> <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b> <a href='{DEVELOPER_URL}'>{DEVELOPER_NAME}</a> (<code>@{DEVELOPER_USERNAME}</code>)</blockquote>\n\n<i>DM Admin or Developer for inquiries, custom bots, or assistance.</i>"
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Support ({SUPPORT_NAME})', url=SUPPORT_URL, icon_custom_emoji_id='6336811288437460963')
    kb.button(text=f'Developer ({DEVELOPER_NAME})', url=DEVELOPER_URL, icon_custom_emoji_id='5269617636001460986')
    kb.button(text=NETWORK_NAME, url=NETWORK_URL, icon_custom_emoji_id='5949775417274536507')
    kb.adjust(2, 1)
    await message.answer(text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('leaderboard_'))
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def show_leaderboard(call: CallbackQuery):
    ga_id = call.data.split('_')[1]
    pipeline = [{'$match': {'ga_id': ga_id}}, {'$sort': {'vote_count': -1}}, {'$limit': 10}]
    cursor = participants_col.aggregate(pipeline)
    text = f"<tg-emoji emoji-id='5204046146955153467'>🏆</tg-emoji> <b>LEADERBOARD (Top 10)</b>\n\n"
    i = 1
    async for p in cursor:
        paid_info = f" (Paid: {p.get('paid_votes_count', 0)})" if p.get('paid_votes_count', 0) > 0 else ''
        safe_name = html.quote(p['name'])
        text += f"{i}. {safe_name} - <b>{p['vote_count']}</b>{paid_info}\n"
        i += 1
    if i == 1:
        text += 'No participants yet.\n\n'
    else:
        text += '\n'
    text += "{POWERED_BY_TEXT}"
    try:
        await call.message.edit_caption(caption=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Back', callback_data=f'my_ga')]]))
    except Exception as e:
        await call.answer('Could not load leaderboard.', show_alert=True)
        logging.error(f'Leaderboard Error: {e}')

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data == 'my_ga')
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def my_ga_dashboard(call: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text='✍️ Created (Active)', callback_data='my_cr_active_0', style='primary')
    kb.button(text='📜 Created (Past)', callback_data='my_cr_past_0', style='primary')
    kb.adjust(2, 2)
    kb.button(text='🤝 Joined (Active)', callback_data='my_jn_active_0', style='primary')
    kb.button(text='📂 Joined (Past)', callback_data='my_jn_past_0', style='primary')
    kb.adjust(2, 2)
    kb.button(text='🔙 Back', callback_data='back_to_start', style='danger')
    kb.adjust(2, 2, 1)
    await call.message.edit_caption(caption="<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <b>My Giveaways</b>\nSelect a category:", reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('my_cr_'))
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def list_created_gas(call: CallbackQuery):
    parts = call.data.split('_')
    mode = parts[2]
    page = int(parts[3])
    user_id = call.from_user.id
    limit = 5
    skip = page * limit
    base_query = {'creator_id': user_id}
    if mode == 'active':
        base_query['status'] = 'active'
        title_text = "<tg-emoji emoji-id='6339289076545358952'>🟢</tg-emoji> Active Created Giveaways"
    else:
        base_query['status'] = {'$ne': 'active'}
        title_text = "<tg-emoji emoji-id='6053019808230805244'>🔴</tg-emoji> Past Created Giveaways"
    total = await giveaways_col.count_documents(base_query)
    cursor = giveaways_col.find(base_query).sort('_id', -1).skip(skip).limit(limit)
    gas = await cursor.to_list(length=limit)
    kb = InlineKeyboardBuilder()
    if not gas:
        kb.button(text='🔙 Back', callback_data='my_ga', style='danger')
        await call.message.edit_caption(caption=f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>No {mode} giveaways found.</b>", reply_markup=kb.as_markup())
        return
    for ga in gas:
        desc = ga.get('description', 'Giveaway')[:20]
        kb.button(text=f'{desc}..', callback_data=f"manage_ga_{ga['ga_id']}")
    kb.adjust(1)
    navs = []
    if page > 0:
        navs.append(InlineKeyboardButton(text='⬅️️', callback_data=f'my_cr_{mode}_{page - 1}'))
    if total > skip + limit:
        navs.append(InlineKeyboardButton(text='➡️️', callback_data=f'my_cr_{mode}_{page + 1}'))
    if navs:
        kb.row(*navs)
    kb.row(InlineKeyboardButton(text='🔙 Back', callback_data='my_ga'))
    await call.message.edit_caption(caption=f"<tg-emoji emoji-id='5395444784611480792'>✍️</tg-emoji> <b>{title_text}</b> (Pg {page + 1})", reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('my_jn_'))
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def list_joined_gas(call: CallbackQuery):
    parts = call.data.split('_')
    mode = parts[2]
    page = int(parts[3])
    user_id = call.from_user.id
    limit = 5
    skip = page * limit
    p_cursor = participants_col.find({'user_id': user_id}).sort('_id', -1)
    user_participations = await p_cursor.to_list(None)
    filtered_ga_ids = []
    for p in user_participations:
        ga = await giveaways_col.find_one({'ga_id': p['ga_id']})
        if not ga:
            continue
        if mode == 'active' and ga['status'] == 'active':
            filtered_ga_ids.append(ga)
        elif mode == 'past' and ga['status'] != 'active':
            filtered_ga_ids.append(ga)
    total = len(filtered_ga_ids)
    paged_gas = filtered_ga_ids[skip:skip + limit]
    kb = InlineKeyboardBuilder()
    title_text = "<tg-emoji emoji-id='6339289076545358952'>🟢</tg-emoji> Active Joined" if mode == 'active' else "<tg-emoji emoji-id='6053019808230805244'>🔴</tg-emoji> Past Joined"
    if not paged_gas:
        kb.button(text='🔙 Back', callback_data='my_ga', style='danger')
        await call.message.edit_caption(caption=f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>No {mode} joined giveaways.</b>", reply_markup=kb.as_markup())
        return
    for ga in paged_gas:
        desc = ga.get('description', 'Giveaway')[:20]
        kb.button(text=f'{desc}..', callback_data=f"view_joined_{ga['ga_id']}")
    kb.adjust(1)
    navs = []
    if page > 0:
        navs.append(InlineKeyboardButton(text='⬅️️', callback_data=f'my_jn_{mode}_{page - 1}'))
    if total > skip + limit:
        navs.append(InlineKeyboardButton(text='➡️️', callback_data=f'my_jn_{mode}_{page + 1}'))
    if navs:
        kb.row(*navs)
    kb.row(InlineKeyboardButton(text='🔙 Back', callback_data='my_ga', style='danger'))
    await call.message.edit_caption(caption=f"<tg-emoji emoji-id='5427168083074628963'>🤝</tg-emoji> <b>{title_text}</b> (Pg {page + 1})", reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('view_joined_'))
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def view_joined_details(call: CallbackQuery):
    ga_id = call.data.split('_')[2]
    user_id = call.from_user.id
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    p = await participants_col.find_one({'ga_id': ga_id, 'user_id': user_id})
    if not ga or not p:
        await call.answer('Data unavailable.', show_alert=True)
        return
    status_icon = "<tg-emoji emoji-id='6339289076545358952'>🟢</tg-emoji> Active" if ga['status'] == 'active' else "<tg-emoji emoji-id='6053019808230805244'>🔴</tg-emoji> Ended"
    text = f"<tg-emoji emoji-id='5409029744693897259'>🎁</tg-emoji> <b>Giveaway Details</b>\n<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Desc:</b> {ga.get('description')}\n\n<tg-emoji emoji-id='5409029744693897259'>📊</tg-emoji> <b>Status:</b> {status_icon}\n<tg-emoji emoji-id='5409029744693897259'>🗳</tg-emoji> <b>Vote Count:</b> {p['vote_count']}\n<tg-emoji emoji-id='5269617636001460986'>👤</tg-emoji> <b>Your Name:</b> {p['name']}\n"
    kb = InlineKeyboardBuilder()
    if ga['status'] == 'active' and ga.get('paid_enabled'):
        kb.button(text='💰 Buy Votes', callback_data=f'buy_start_{ga_id}', style='primary')
    kb.button(text='🏆 Leaderboard', callback_data=f'leaderboard_{ga_id}', style='primary')
    kb.adjust(1)
    kb.button(text='🔗 Get Channel & Post Link', callback_data=f'get_links_{ga_id}', style='primary')
    kb.button(text='🔙 Back', callback_data='my_ga', style='danger')
    await call.message.edit_caption(caption=text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('manage_ga_'))
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def manage_ga_menu(call: CallbackQuery):
    ga_id = call.data.split('_')[2]
    ga = await giveaways_col.find_one({'ga_id': ga_id})
    text = f"<tg-emoji emoji-id='5341715473882955310'><tg-emoji emoji-id='5341715473882955310'>⚙️</tg-emoji>️</tg-emoji> <b>Management Panel</b>\nID: <code>{ga_id}</code>\nStatus: {ga['status']}\nParticipants: {ga.get('participants_count', 0)}\nLink: https://t.me/{BOTUSER}?start={ga_id}"
    kb = InlineKeyboardBuilder()
    kb.button(text='🏆 Leaderboard', callback_data=f'leaderboard_{ga_id}', style='primary')
    if ga['status'] == 'active':
        kb.button(text='🛑 Stop Paid Votes', callback_data=f'act_stoppaid_{ga_id}', style='danger')
        kb.button(text='🛑 Stop Participation', callback_data=f'act_stoppart_{ga_id}', style='danger')
        kb.button(text='🔚 End Giveaway', callback_data=f'act_end_{ga_id}', style='danger')
    kb.button(text='🗑 Clear Channel Posts', callback_data=f'act_clear_{ga_id}', style='danger')
    kb.button(text='🔙 Back', callback_data='my_ga', style='primary')
    kb.adjust(1)
    try:
        media = InputMediaPhoto(media=get_welcome_image(), caption=text)
        await call.message.edit_media(media=media, reply_markup=kb.as_markup())
    except Exception:
        await call.message.delete()
        await call.message.answer_photo(photo=get_welcome_image(), has_spoiler=True, caption=text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('act_'))
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def handle_actions(call: CallbackQuery):
    action, ga_id = (call.data.split('_')[1], call.data.split('_')[2])
    if action == 'end':
        await end_giveaway_logic(ga_id)
        await call.answer('Giveaway Ended!', show_alert=True)
    elif action == 'stoppaid':
        await giveaways_col.update_one({'ga_id': ga_id}, {'$set': {'paid_enabled': False}})
        await call.answer('Paid votes disabled.', show_alert=True)
    elif action == 'stoppart':
        await giveaways_col.update_one({'ga_id': ga_id}, {'$set': {'status': 'participation_stopped'}})
        await call.answer('Participation stopped.', show_alert=True)
    elif action == 'clear':
        await call.answer('Deleting posts... this may take time.')
        parts = participants_col.find({'ga_id': ga_id})
        count = 0
        async for p in parts:
            try:
                await bot.delete_message(chat_id=p['channel_id'], message_id=p['msg_id'])
                count += 1
                await asyncio.sleep(0.05)
            except:
                pass
        await call.message.answer(f"<tg-emoji emoji-id='5445267414562389170'>🗑</tg-emoji> <b>Cleared {count} posts from channel.</b>")
    await manage_ga_menu(call)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('setposttext'))
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def set_post_text_command(message: Message):
    if message.from_user.id not in OWNER_IDS:
        return
    full_html = message.html_text
    parts = full_html.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> <b>Usage:</b>\n<code>/setposttext [Your Custom Message]</code>\n\n<b>Available Variables:</b>\n<code>{channel}</code> - Shows Channel Name\n<code>{user}</code> - Shows User Name\n<code>{link}</code> - Shows Channel Link (if public)\n\n<i>You can use HTML tags, Blockquotes, Bold, etc.</i>")
        return
    custom_text = parts[1]
    await settings_col.update_one({'_id': 'on_admin_add_text'}, {'$set': {'text': custom_text}}, upsert=True)
    await message.answer(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Welcome Message Updated!</b>\n\n<b>Preview of saved text:</b>\n{custom_text}", disable_web_page_preview=True)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def on_bot_added_as_admin(event: ChatMemberUpdated):
    """
    Triggered when Bot is promoted to Admin.
    1. Saves channel to DB.
    2. Sends CUSTOM message to user.
    """
    new_chat = event.chat
    user = event.from_user
    await channels_col.update_one({'chat_id': new_chat.id}, {'$set': {'chat_id': new_chat.id, 'title': new_chat.title, 'username': new_chat.username, 'type': new_chat.type, 'added_by': user.id, 'updated_at': datetime.now()}}, upsert=True)
    setting = await settings_col.find_one({'_id': 'on_admin_add_text'})
    if setting and setting.get('text'):
        text_template = setting.get('text')
    else:
        text_template = "<tg-emoji emoji-id='5461151367559141950'>🎉</tg-emoji> <b>Thanks for adding me!</b>\n\nI am now an Admin in: <b>{channel}</b>\n\nYou can now use /createpost to publish messages."
    channel_name = html.quote(new_chat.title)
    user_name = html.quote(user.full_name)
    chat_link = f'https://t.me/{new_chat.username}' if new_chat.username else 'No Public Link'
    final_text = text_template.replace('{channel}', channel_name).replace('{user}', user_name).replace('{link}', chat_link)
    try:
        kb = InlineKeyboardBuilder()
        if new_chat.username:
            kb.button(text='↗️ Go to Channel', url=chat_link)
        await bot.send_message(chat_id=user.id, text=final_text, reply_markup=kb.as_markup(), disable_web_page_preview=True)
    except Exception as e:
        logging.warning(f'Could not DM user {user.id}: {e}')

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('createpost'))
@router.callback_query(F.data == 'create_post_start')
# [Module Component: Developed & Built by Aryan | https://t.me/thatonearyan]
async def post_start_unified(event: Union[Message, CallbackQuery], state: FSMContext):
    await state.clear()
    await state.set_state(PostMaker.waiting_for_media)
    caption_text = "<tg-emoji emoji-id='5427168083074628963'>📸</tg-emoji> <b>Create New Post: Step 1</b>\n\nSend a <b>Photo</b> to include in your post.\nOr click <b>Skip Media</b> for a text-only post."
    kb = InlineKeyboardBuilder()
    kb.button(text='⏭ Skip Media', callback_data='post_skip_media', style='primary')
    kb.button(text='🔙 Cancel', callback_data='back_to_start', style='danger')
    if isinstance(event, Message):
        await event.answer(caption_text, reply_markup=kb.as_markup())
    else:
        try:
            await event.message.edit_caption(caption=caption_text, reply_markup=kb.as_markup())
        except:
            await event.message.delete()
            await event.message.answer(caption_text, reply_markup=kb.as_markup())

@router.callback_query(F.data == 'post_skip_media', PostMaker.waiting_for_media)
# [System Routine: Designed & Implemented by Aryan - https://t.me/thatonearyan]
async def post_skip_media(call: CallbackQuery, state: FSMContext):
    await state.update_data(media_file_id=None, media_type='text')
    await call.message.delete()
    await call.message.answer("<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Step 2: Send Caption</b>\n\nSend the text for your post.\nFormatting (Bold, Italic, HTML) will be preserved.")
    await state.set_state(PostMaker.waiting_for_caption)

@router.message(PostMaker.waiting_for_media)
# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]
async def post_receive_media(message: Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        await state.update_data(media_file_id=file_id, media_type='photo')
        await message.answer("<tg-emoji emoji-id='5395444784611480792'>📝</tg-emoji> <b>Step 2: Send Caption</b>\n\nSend the text for your post.\nFormatting will be preserved.")
        await state.set_state(PostMaker.waiting_for_caption)
    else:
        await message.answer("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Please send a Photo or click Skip.")

@router.message(PostMaker.waiting_for_caption)
# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def post_receive_caption(message: Message, state: FSMContext):
    caption_text = message.html_text
    await state.update_data(caption=caption_text)
    await message.answer('🔘 <b>Step 3: Add Buttons</b>\n\nSend buttons in this format:\n<code>Name - Link</code>\n\n<b>For multiple buttons in one row, use && :</b>\n<code>Btn1 - Link1 && Btn2 - Link2</code>\n<code>Btn3 - Link3</code>\n\nType /skip to send without buttons.', disable_web_page_preview=True)
    await state.set_state(PostMaker.waiting_for_buttons)

@router.message(PostMaker.waiting_for_buttons)
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def post_receive_buttons(message: Message, state: FSMContext):
    text = message.text.strip()
    kb = InlineKeyboardBuilder()
    if text != '/skip':
        rows = text.split('\n')
        row_widths = []
        try:
            for row in rows:
                if not row.strip():
                    continue
                btns = row.split('&&')
                row_widths.append(len(btns))
                for btn in btns:
                    if '-' in btn:
                        label, url = btn.split('-', 1)
                        kb.button(text=label.strip(), url=url.strip())
                    else:
                        await message.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Invalid format: {btn}")
                        return
            kb.adjust(*row_widths)
        except Exception as e:
            await message.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Error parsing buttons: {e}")
            return
    markup = kb.as_markup()
    await state.update_data(reply_markup=markup)
    data = await state.get_data()
    control_kb = InlineKeyboardBuilder()
    control_kb.button(text='🚀 Send to Channel', callback_data='post_select_channel')
    control_kb.button(text='🗑 Discard', callback_data='back_to_start')
    control_kb.adjust(1)
    await message.answer('👀 <b>Preview:</b>')
    try:
        if data['media_type'] == 'photo':
            await message.answer_photo(photo=data['media_file_id'], caption=data['caption'], reply_markup=markup)
        else:
            await message.answer(text=data['caption'], reply_markup=markup, disable_web_page_preview=True)
        await message.answer('👆 <b>This is your preview.</b>\nReady to publish?', reply_markup=control_kb.as_markup())
    except Exception as e:
        await message.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Error generating preview: {e}")

@router.callback_query(F.data == 'post_select_channel')
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def post_choose_channel_start(call: CallbackQuery, state: FSMContext):
    await show_channel_selection(call, page=0)

@router.callback_query(F.data.startswith('post_page_'))
# [State & Workflow Engine: Programmed by Aryan (@thatonearyan | https://t.me/thatonearyan)]
async def post_choose_channel_page(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split('_')[2])
    await show_channel_selection(call, page=page)

# [Interactive Telegram UI System: Developed by Aryan | https://t.me/thatonearyan]
async def show_channel_selection(call: CallbackQuery, page: int):
    user_id = call.from_user.id
    ITEMS_PER_PAGE = 10
    unique_chats = {}
    async for ch in channels_col.find({'added_by': user_id}):
        unique_chats[ch['chat_id']] = ch['title']
    async for ga in giveaways_col.find({'creator_id': user_id}):
        c_id = ga.get('target_channel_id')
        if c_id and c_id not in unique_chats:
            unique_chats[c_id] = ga.get('target_channel_title', str(c_id))
    valid_chats = []
    all_ids = sorted(unique_chats.keys())
    for ch_id in all_ids:
        try:
            bot_member = await bot.get_chat_member(ch_id, bot.id)
            if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                continue
            user_member = await bot.get_chat_member(ch_id, user_id)
            if user_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                continue
            title = unique_chats[ch_id]
            if str(title).startswith('-100') or str(title).isdigit():
                try:
                    chat_info = await bot.get_chat(ch_id)
                    title = chat_info.title
                except:
                    pass
            valid_chats.append({'id': ch_id, 'title': title})
        except Exception:
            continue
    if not valid_chats:
        kb = InlineKeyboardBuilder()
        kb.button(text='➕ How to add?', callback_data='noop')
        kb.button(text='🔙 Back', callback_data='back_to_start')
        await call.message.edit_text("<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> <b>No Accessible Channels Found.</b>\n\n1. Add this bot to your Channel.\n2. Promote it to <b>Admin</b>.\n3. Try again.\n\n<i>Only channels where BOTH you and the bot are admins will appear here.</i>", reply_markup=kb.as_markup())
        return
    total_items = len(valid_chats)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if page >= total_pages:
        page = total_pages - 1
    if page < 0:
        page = 0
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_batch = valid_chats[start_idx:end_idx]
    kb = InlineKeyboardBuilder()
    for chat in current_batch:
        kb.button(text=f"<tg-emoji emoji-id='5424818078833715060'>📢</tg-emoji> {chat['title']}", callback_data=f"publish_{chat['id']}")
    kb.adjust(1)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text='⬅️️', callback_data=f'post_page_{page - 1}'))
    nav_buttons.append(InlineKeyboardButton(text=f'{page + 1}/{total_pages}', callback_data='noop'))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text='➡️️', callback_data=f'post_page_{page + 1}'))
    kb.row(*nav_buttons)
    kb.row(InlineKeyboardButton(text='🔙 Cancel', callback_data='back_to_start'))
    msg_text = '📤 <b>Select Destination Channel:</b>'
    try:
        await call.message.edit_text(msg_text, reply_markup=kb.as_markup())
    except:
        await call.message.delete()
        await call.message.answer(msg_text, reply_markup=kb.as_markup())

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.callback_query(F.data.startswith('publish_'))
# [Core Logic & Architecture Engineered by Aryan (@thatonearyan)]
async def post_publish(call: CallbackQuery, state: FSMContext):
    try:
        target_id = int(call.data.split('_')[1])
        data = await state.get_data()
        if data['media_type'] == 'photo':
            await bot.send_photo(chat_id=target_id, photo=data['media_file_id'], caption=data['caption'], reply_markup=data.get('reply_markup'))
        else:
            await bot.send_message(chat_id=target_id, text=data['caption'], reply_markup=data.get('reply_markup'), disable_web_page_preview=True)
        kb = InlineKeyboardBuilder()
        kb.button(text='✅ Posted! Send Another?', callback_data='create_post_start')
        kb.button(text='🏠 Home', callback_data='back_to_start')
        kb.adjust(1)
        await call.message.delete()
        await call.message.answer("<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Post published successfully!</b>", reply_markup=kb.as_markup())
        await state.clear()
    except Exception as e:
        await call.answer(f"<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Failed: {str(e)}", show_alert=True)

# Handler Authored by Aryan (@thatonearyan | https://t.me/thatonearyan)
@router.message(Command('broadcast'))
# [Handler Execution Pipeline: Developed by Aryan | Telegram: @thatonearyan]
async def broadcast_command(message: Message):
    if message.from_user.id not in OWNER_IDS:
        return
    if not message.reply_to_message:
        await message.answer("<tg-emoji emoji-id='5395695537687123235'>⚠️</tg-emoji> <b>Error:</b> Please reply to the message you want to broadcast.")
        return
    source_msg = message.reply_to_message
    status_msg = await message.answer('🚀 <b>Broadcast started...</b>\n<i>Do not delete the original message.</i>')
    success = 0
    blocked = 0
    total = 0
    users = users_col.find({})
    async for user in users:
        total += 1
        user_id = user.get('user_id')
        if not user_id:
            continue
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=source_msg.chat.id, message_id=source_msg.message_id, reply_markup=source_msg.reply_markup)
            success += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            blocked += 1
        if total % 200 == 0:
            try:
                await status_msg.edit_text(f"🚀 <b>Broadcasting...</b>\n<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> Sent: {success}\n<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Failed: {blocked}\n<tg-emoji emoji-id='5409029744693897259'>📊</tg-emoji> Total Checked: {total}")
            except:
                pass
    await status_msg.edit_text(f"<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> <b>Broadcast Completed!</b>\n\n<tg-emoji emoji-id='5269617636001460986'>👥</tg-emoji> Total Users: {total}\n<tg-emoji emoji-id='6339289076545358952'>✅</tg-emoji> Success: {success}\n<tg-emoji emoji-id='6053019808230805244'>❌</tg-emoji> Failed/Blocked: {blocked}")

# [Security & Database Layer: Built by Aryan - https://t.me/thatonearyan]

# ---------------- BOT DESCRIPTION & ABOUT ENFORCER ---------------- #
# [Security & Anti-Tamper Routine: Developed by Aryan | https://t.me/thatonearyan]
BOT_TAGLINE = os.getenv("BOT_TAGLINE", "Fair & Automated Giveaway Bot\\n!ᵎ! TRUST • POWER • INNOVATION ✦")
CUSTOM_BOT_DESCRIPTION = os.getenv("CUSTOM_BOT_DESCRIPTION", "")
CUSTOM_BOT_ABOUT = os.getenv("CUSTOM_BOT_ABOUT", "")

async def enforce_bot_description():
    try:
        if CUSTOM_BOT_DESCRIPTION:
            desc_text = CUSTOM_BOT_DESCRIPTION.replace("\\n", "\n").strip()
        else:
            desc_text = (
                f"𖤍 — POWERED BY {NETWORK_NAME.upper()} ⚡️\\n\\n"
                f"👑 OWNER — {SUPPORT_NAME.upper()} (@{SUPPORT_USERNAME})\\n"
                f"👨‍💻 DEVELOPER — ARYAN (@ThatOnearyan)\\n\\n"
                f"🎁 {BOT_TAGLINE}"
            )
        if CUSTOM_BOT_ABOUT:
            short_desc = CUSTOM_BOT_ABOUT.replace("\\n", "\n").strip()
        else:
            short_desc = f"{BRAND_NAME} Giveaway Bot | Developed by @ThatOnearyan"
        await bot.set_my_description(description=desc_text)
        await bot.set_my_short_description(short_description=short_desc)
    except Exception as e:
        logger.warning(f"Could not update bot description/about: {e}")

async def main():
    await enforce_bot_description()
    scheduler.add_job(enforce_bot_description, 'interval', minutes=30)
    scheduler.add_job(run_global_resync, 'interval', minutes=1)
    scheduler.add_job(clean_expired_global_channels, 'interval', minutes=30)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot is running with Auto-Resync (2 min)...')
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())