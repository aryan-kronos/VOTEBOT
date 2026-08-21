# 🎬 VOTEBOT — Silent Screen Recording Video Script & Walkthrough

This guide is designed for a **silent video recording** (no voiceover needed). Simply follow the actions step-by-step on screen while recording.

---

## 🖥️ Screen Layout Setup Before You Record

Split your monitor into two sides:
- **👈 LEFT SIDE**: **VS Code** (Top) + **Terminal** (Bottom)
- **👉 RIGHT SIDE**: **Telegram Desktop App**

---

## ⏱️ Scene-by-Scene Visual Walkthrough

---

### 🔹 STEP 1: Terminal & Repository Setup (Left Side)

1. Open **Terminal** on the bottom-left and paste:
   ```bash
   cd ~/Desktop
   git clone https://github.com/Aryan-dot-sketch/VOTEBOT.git
   cd VOTEBOT
   ```
2. Create and activate the Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template:
   ```bash
   cp env.example .env
   ```

---

### 🔹 STEP 2: Configure `.env` in VS Code (Top-Left Side)

1. In **VS Code**, open the `VOTEBOT` folder and click on `.env`.
2. Slowly scroll through `.env` to visually show how everything is configurable:
   - **Bot Token**: `BOT_TOKEN=...`
   - **Bot Username**: `BOT_USERNAME=...`
   - **Admin IDs**: `ADMINS=...`
   - **MongoDB URI**: `MONGO_URI=...`
   - **Custom Branding**: `BRAND_NAME=...`, `SUPPORT_NAME=...`, `DEFAULT_UPI_ID=...`
3. Save `.env` (`Cmd + S`).

---

### 🔹 STEP 3: Start the Bot in Terminal (Bottom-Left Side)

1. Run the bot in Terminal:
   ```bash
   python bot.py
   ```
2. Wait 2 seconds so the clean startup logs appear on screen:
   ```text
   INFO:apscheduler.scheduler:Added job "enforce_bot_description" to job store "default"
   INFO:apscheduler.scheduler:Added job "run_global_resync" to job store "default"
   INFO:apscheduler.scheduler:Scheduler started
   INFO:aiogram.dispatcher:Start polling
   INFO:aiogram.dispatcher:Run polling for bot @YourBot
   ```

---

### 🔹 STEP 4: Live Bot Showcase on Telegram (Right Side)

Switch focus to **Telegram** on the right side:

1. **Show Start Card (Before Pressing Start)**:
   - Highlight the description box showing:
     - `👑 OWNER — DEVANSH (@tgbitz_op)`
     - `👨‍💻 DEVELOPER — ARYAN (@ThatOnearyan)`
     - `🎁 Fair & Automated Giveaway Bot`

2. **Press `Start` (or send `/start`)**:
   - Show the welcome banner image and custom animated sticker emojis.
   - Click the **`👨‍💻 Developer (Aryan)`** button (shows instant redirect to `@thatonearyan`).

3. **Demonstrate Dynamic UPI QR Code (`Membership`)**:
   - Click **`💎 Membership`** (or send `/membership`).
   - Click on **`7 Days - ₹49`**.
   - Show the real-time dynamic QR code generated instantly with `₹49` encoded.

4. **Demonstrate Admin Panel (`/settings`)**:
   - Send `/settings` in chat.
   - Click **`💳 Change UPI ID`** to show interactive prompt.
   - Click **`💎 Edit VIP Prices`** to show plan duration configuration.
   - Click **`🔙 Back to Settings`**.

5. **Demonstrate Giveaway Creation**:
   - Click **`➕ New Giveaway`**.
   - Type a title (e.g. `Test iPhone Giveaway`) and send `/skip` for thumbnail.
   - Show how cleanly the bot prompts for target channel selection.

6. **Demonstrate Bot Stats (`/stats`)**:
   - Send `/stats`.
   - Show the analytics card with total users, active giveaways, and Developer credit.

---

### 🔹 STEP 5: Ending Screen

1. Open your browser or VS Code showing the GitHub repository:
   **`https://github.com/Aryan-dot-sketch/VOTEBOT.git`**
2. Hover over the Star button or README header.
3. Stop recording! 🎉

---

## 📋 Quick Copy-Paste Command Sheet for Terminal

```bash
cd ~/Desktop/VOTEBOT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
python bot.py
```
