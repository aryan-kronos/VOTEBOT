<div align="center">

# 🚀 VOTEBOT — Modular Telegram Giveaway & Voting Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Motor%20Async-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Developer](https://img.shields.io/badge/Developer-Aryan-FF6B6B?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/thatonearyan)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**An enterprise-grade, high-performance Telegram Giveaway, Voting, and VIP Membership Engine built with Python 3, aiogram 3.x, and MongoDB (Motor).**

[Features](#-key-features) • [Installation](#-quick-start) • [Configuration](#-environment-variables) • [Deployment](#-deployment--production) • [Developer](#-developer--support)

---

</div>

## 🌟 Overview

**VOTEBOT** is an all-in-one Telegram bot designed for communities, channels, and brands to host interactive giveaways, track verified votes with anti-cheat protections, sell VIP memberships with dynamic UPI QR code payments, and rebrand the entire system with **zero code modifications** directly from `.env`.

---

## ⚡ Key Features

- 🎁 **Full Giveaway & Voting Engine**:
  - Create channel and group giveaways with custom thumbnails, end timers, and automatic winner selection.
  - Generates dedicated participant voting cards with live vote counters and shareable referral links.
- 💳 **Dynamic Real-Time UPI QR Code Generator**:
  - Automatically generates dynamic QR codes on-the-fly with the exact price and customized UPI note encoded.
  - Full screenshot upload and in-chat 1-tap **Approve / Reject** admin workflow.
- 💎 **Tiered VIP Membership System**:
  - Customizable subscription durations (e.g. 7-Day, 15-Day, 30-Day plans).
  - Unlocks custom giveaway thumbnails, extra force-sub channels, and automated vote protection.
- 🛡️ **Anti-Cheat & Global Channel Resync**:
  - Automated background task verifies that voters stay subscribed to required channels.
  - Automatically deducts votes in real time if a voter leaves any linked channel.
- 🔒 **Permanent Anti-Tamper Developer Enforcer**:
  - Periodically synchronizes and locks the bot description ("What can this bot do?" start window) and profile About text via the Telegram Bot API.
- 🎨 **Animated Telegram Custom Sticker Emojis**:
  - Rich user interface utilizing verified animated custom emoji sticker tags (`<tg-emoji>`).
- ⚙️ **Interactive In-Bot Admin Dashboard (`/settings`)**:
  - Modify UPI ID, change VIP plan prices, update start messages, and set winner templates directly from chat.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/aryan-kronos/VOTEBOT.git
cd VOTEBOT
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv venv

# On Linux / macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template file to `.env`:
```bash
cp env.example .env
```

Open `.env` and fill in your bot credentials and branding:
```env
# Bot Credentials
BOT_TOKEN=your_bot_token_from_botfather
BOT_USERNAME=your_bot_username

# Admin IDs (Comma-separated)
ADMINS=123456789,987654321

# Database
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=Votebot

# Dynamic Branding
BRAND_NAME=BITZ
BRAND_NAME_SMALLCAPS=ʙɪᴛᴢ
BOT_NAME=BITZ GIVEAWAY BOT
BOT_NAME_STYLED=𝐁𝐈𝐓𝐙 𝐆𝐈𝐕𝐄𝐀𝐖𝐀𝐘 𝐁𝐎𝐓!
NETWORK_NAME=ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ
NETWORK_USERNAME=tgbitz
SUPPORT_NAME=ᴅᴇᴠᴀɴꜱʜ
SUPPORT_USERNAME=tgbitz_op
DEFAULT_UPI_ID=your_upi_id@bank
```

### 5. Launch the Bot
```bash
python bot.py
```

---

## 📋 Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `BOT_TOKEN` | Telegram Bot Token from [@BotFather](https://t.me/BotFather) | *Required* |
| `BOT_USERNAME` | Bot Username (without `@`) | `YourVoteBot` |
| `ADMINS` | Comma-separated Telegram User IDs for Admin panel access | *Required* |
| `MONGO_URI` | MongoDB Connection String (Atlas or Local) | `mongodb://localhost:27017` |
| `DATABASE_NAME`| MongoDB Database Name | `Votebot` |
| `LOG_CHANNEL_ID` | Telegram Channel ID for bot logs (`-100...`) | `0` |
| `BRAND_NAME` | Brand title used across templates | `BITZ` |
| `BOT_NAME_STYLED` | Styled Unicode title for start screen | `𝐁𝐈𝐓𝐙 𝐆𝐈𝐕𝐄𝐀𝐖𝐀𝐘 𝐁𝐎𝐓!` |
| `NETWORK_NAME` | Community / Network Name | `ʙɪᴛᴢ ɴᴇᴛᴡᴏʀᴋ` |
| `NETWORK_USERNAME` | Community / Channel Username | `tgbitz` |
| `SUPPORT_NAME` | Support Lead Name | `ᴅᴇᴠᴀɴꜱʜ` |
| `SUPPORT_USERNAME` | Support Telegram Username | `tgbitz_op` |
| `DEFAULT_UPI_ID` | Default UPI ID for payments | `devanshsingh2@fam` |
| `DEFAULT_PLANS` | Default VIP Pricing format (`Days Price Days Price...`) | `7D 49 15D 89 30D 149` |
| `BOT_TAGLINE` | Tagline shown in start description box | `Fair & Automated Giveaway Bot` |

---

## 🛠️ Deployment & Production

### Running as a Systemd Service (Ubuntu / Debian VPS)

1. Create a service file:
```bash
sudo nano /etc/systemd/system/votebot.service
```

2. Add the following configuration:
```ini
[Unit]
Description=VOTEBOT Telegram Bot Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/VOTEBOT
ExecStart=/home/ubuntu/VOTEBOT/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable votebot
sudo systemctl start votebot
sudo systemctl status votebot
```

---

## 📁 Repository Structure

```text
VOTEBOT/
├── assets/
│   └── welcome.jpg           # Default welcome banner image
├── bot.py                    # Main bot engine, handlers & scheduler
├── config.py                 # Clean configuration loader
├── database.py               # Motor MongoDB Async models & collections
├── states.py                 # FSM State definitions
├── env.example               # Template environment configuration (visible)
├── example.env               # Secondary visible env example
├── env_template.txt          # Plaintext env template
├── .env.example              # Standard hidden git template
├── .gitignore                # Production git ignore rules
├── Procfile                  # Process definition for PaaS hosting
├── runtime.txt               # Python runtime version specification
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## 👨‍💻 Developer & Support

- **Lead Developer**: **Aryan**
- **Telegram Contact**: [@thatonearyan](https://t.me/thatonearyan)
- **GitHub Repository**: [Aryan-dot-sketch/VOTEBOT](https://github.com/Aryan-dot-sketch/VOTEBOT.git)

---

<div align="center">
<b>Made with ❤️ by <a href="https://t.me/thatonearyan">Aryan</a></b>
</div>
