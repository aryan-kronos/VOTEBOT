# 📖 Complete Setup & Deployment Guide for VOTEBOT

This document provides a comprehensive, step-by-step guide to installing, configuring, running, and hosting **VOTEBOT** from scratch.

---

## 📋 Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Step 1: Get Telegram Bot Token & User IDs](#step-1-get-telegram-bot-token--user-ids)
3. [Step 2: Create a Free MongoDB Database](#step-2-create-a-free-mongodb-database)
4. [Step 3: Clone and Install Dependencies](#step-3-clone-and-install-dependencies)
5. [Step 4: Configure Environment Variables (.env)](#step-4-configure-environment-variables-env)
6. [Step 5: Telegram Channel & Group Permissions](#step-5-telegram-channel--group-permissions)
7. [Step 6: Run and Test Locally](#step-6-run-and-test-locally)
8. [Step 7: 24/7 Production Deployment on VPS](#step-7-247-production-deployment-on-vps)
9. [Step 8: Admin Commands & Controls](#step-8-admin-commands--controls)
10. [Troubleshooting & FAQ](#troubleshooting--faq)

---

## 1. Prerequisites

Before starting, ensure you have:
- **Python 3.10 or higher** installed (`python3 --version` or `python --version`).
- **Git** installed (`git --version`).
- A **Telegram Account**.
- A **MongoDB Atlas Account** (Free cloud tier available) or a local MongoDB server.

---

## Step 1: Get Telegram Bot Token & User IDs

### A. Create Your Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot`.
3. Choose a **Name** for your bot (e.g. `My Giveaway Bot`).
4. Choose a **Username** ending in `bot` (e.g. `MyVoteGiveawayBot`).
5. @BotFather will provide an **API Token** (Format: `1234567890:ABCdefGHIjklMNOpqrSTUvwxyz`). **Copy and save this token.**

### B. Get Your Telegram User ID
1. Search for [@userinfobot](https://t.me/userinfobot) or [@MissRose_bot](https://t.me/MissRose_bot) on Telegram.
2. Send `/start` or `/id`.
3. Copy your numeric **User ID** (e.g. `233444460`). This will be added to `ADMINS` in `.env`.

---

## Step 2: Create a Free MongoDB Database

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) and create a free account.
2. Build a new free **M0 Shared Cluster**.
3. Under **Database Access**:
   - Create a database user (e.g. `botuser`) and a secure password.
4. Under **Network Access**:
   - Add IP Address: `0.0.0.0/0` (Allow access from anywhere).
5. Go to **Clusters** > Click **Connect** > Choose **Drivers** (Python).
6. Copy your connection string:
   ```text
   mongodb+srv://botuser:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   *(Replace `<password>` with your actual database user password)*.

---

## Step 3: Clone and Install Dependencies

Open your terminal or command prompt:

```bash
# 1. Clone the repository
git clone https://github.com/Aryan-dot-sketch/VOTEBOT.git
cd VOTEBOT

# 2. Create Python virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
# On macOS / Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 4. Install all required dependencies
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables (`.env`)

Copy the provided `env.example` file to create your `.env`:

```bash
cp env.example .env
```

Open `.env` in any text editor and fill in your values:

```env
# ================================================================
# 🤖 BOT CREDENTIALS
# ================================================================
BOT_TOKEN=your_bot_token_from_botfather
BOT_USERNAME=your_bot_username_without_at

# ================================================================
# 👑 ADMINISTRATORS
# ================================================================
# Comma-separated Telegram User IDs who have full Owner/Admin access
ADMINS=233444460,8295433038,8021449673

# ================================================================
# 🗄️ DATABASE
# ================================================================
MONGO_URI=mongodb+srv://botuser:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=Votebot

# ================================================================
# 📢 CHANNELS & LOGGING (Optional)
# ================================================================
LOG_CHANNEL_ID=-1001234567890

# ================================================================
# 🎨 CUSTOM BRANDING & REBRANDING (100% Configurable)
# ================================================================
BRAND_NAME=BITZ
BRAND_NAME_SMALLCAPS=ʙɪᴛᴢ
BOT_NAME=BITZ GIVEAWAY BOT
BOT_NAME_STYLED=𝐁𝐈𝐓𝐙 𝐆𝐈𝐕𝐄𝐀𝐖𝐀𝐘 𝐁𝐎𝐓!

# Network / Community Link
NETWORK_NAME=ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ
NETWORK_USERNAME=tgbitz
NETWORK_URL=https://t.me/tgbitz

# Support Contact
SUPPORT_NAME=ᴅᴇᴠᴀɴꜱʜ
SUPPORT_USERNAME=tgbitz_op
SUPPORT_URL=https://t.me/tgbitz_op

# Start Guide / How To Use Link
HOW_TO_USE_URL=https://t.me/tgbitz

# Payment UPI ID for VIP memberships & Dynamic QR codes
DEFAULT_UPI_ID=devanshsingh2@fam

# VIP Pricing Structure (Format: Days Price Days Price...)
DEFAULT_PLANS=7D 49 15D 89 30D 149
```

---

## Step 5: Telegram Channel & Group Permissions

For the bot to post giveaways, verify memberships, and manage votes:

1. **Add the Bot to your Target Channel**:
   - Open your Telegram Channel > Channel Info > Administrators.
   - Click **Add Administrator** > Search for your bot username.
   - Grant permissions:
     - ✅ **Post Messages**
     - ✅ **Edit Messages**
     - ✅ **Invite Users via Link**
2. **Add the Bot to your Force-Sub Channels / Groups**:
   - Add the bot as Admin so it can check member statuses in real time.

---

## Step 6: Run and Test Locally

To start the bot:

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run bot
python bot.py
```

### Verification Checklist:
- Open Telegram and search your bot.
- Check the start description card (should show your custom brand + permanent developer Aryan credit).
- Click **Start** (`/start`).
- Check that the interactive buttons load with animated custom emojis.
- Send `/settings` (if you are in `ADMINS`) to verify the admin control panel.

---

## Step 7: 24/7 Production Deployment on VPS

To keep the bot running 24/7 on a Linux VPS (Ubuntu / Debian):

### 1. Connect to your VPS & Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y

git clone https://github.com/Aryan-dot-sketch/VOTEBOT.git
cd VOTEBOT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
nano .env  # Enter your credentials and save with Ctrl+O, Ctrl+X
```

### 2. Create a Systemd Background Service
```bash
sudo nano /etc/systemd/system/votebot.service
```

Paste the following:
```ini
[Unit]
Description=VOTEBOT 24/7 Telegram Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/VOTEBOT
ExecStart=/root/VOTEBOT/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
*(Adjust `/root/VOTEBOT` to your actual folder path if different)*.

### 3. Enable and Start the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable votebot
sudo systemctl start votebot

# Check live logs & status
sudo systemctl status votebot
sudo journalctl -u votebot -f
```

---

## Step 8: Admin Commands & Controls

| Command | Role | Description |
| :--- | :--- | :--- |
| `/start` | Public | Opens main menu, giveaways, guides & developer contact |
| `/settings` | Admin | In-chat Admin Settings panel (UPI, VIP pricing, Welcome text) |
| `/setupi <upi_id>` | Admin | Change the default payment UPI ID dynamically |
| `/setprices 7D 50 30D 150` | Admin | Update VIP membership plan durations and prices |
| `/setwin <text>` | Admin | Set custom winner announcement message template |
| `/setstart` | Admin | Update custom `/start` caption while preserving emojis |
| `/stats` | Admin | View real-time user count, active giveaways, and top creators |
| `/membership` | Public | View VIP plans, features, and buy membership via QR |
| `/support` | Public | Contact support lead & developer Aryan |

---

## Troubleshooting & FAQ

### 1. `TelegramBadRequest: Chat not found` or `Bot is not an admin`
- **Fix**: Ensure the bot is added as an **Administrator** with *Post Messages* permission in the target channel.

### 2. `ServerSelectionTimeoutError` (MongoDB Connection)
- **Fix**: Go to MongoDB Atlas > Network Access > ensure IP `0.0.0.0/0` is added to the IP Access List.

### 3. Why are `.env` files hidden on Mac?
- **Fix**: Press `Cmd + Shift + .` in macOS Finder to toggle hidden files, or use the included `env.example` / `env_template.txt`.

### 4. Can developer credit be removed via `.env`?
- **No**: Developer attribution for **Aryan** ([@thatonearyan](https://t.me/thatonearyan)) is permanently hardcoded in the engine and protected with an automated anti-tamper Bot API synchronizer.

---

## 👨‍💻 Support & Contact

- **Lead Developer**: **Aryan**
- **Telegram**: [@thatonearyan](https://t.me/thatonearyan)
- **GitHub Repository**: [Aryan-dot-sketch/VOTEBOT](https://github.com/Aryan-dot-sketch/VOTEBOT.git)

---

*Enjoy hosting smooth, automated, and secure giveaways with VOTEBOT!*
