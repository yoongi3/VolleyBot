# VolleyBot

## Introduction
VolleyBot is a Discord bot that helps you find available volleyball courts at [Olympic Park Sports Hall](https://secure.activecarrot.com/public/facility/browse/487/1848). After running a command, it provides you with available booking times. Use this bot to plan and schedule your court bookings.

## Features
- **Court Availability:** Finds court availability at Olympic Park Sports Halls.
- **Weekdays:** Filters out courts that cannot be booked past 7 PM.
- **Weekends:** Shows all available times.

## Commands
- `?courts [X]` : Provides court availability for the next [X] days (default is 7 days).
- `?next [Y] [X]` : Shows court availability starting [Y] weeks ahead for the next [X] days (default is 1 week ahead and 7 days).


Setup Instructions
1. **Clone the Repository:** Clone this repository to your local machine using the following command:
```bash
git clone https://github.com/yoongi3/VolleyBot.git
```

2. **Set up Virtual Environment (Optional/Recommended):**

```bash
# Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate
```
3. **Install Dependencies:** Navigate to the project directory and install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
4. **Set Environment Variables:** Create a '**.env**' file in the project directory and add your Discord bot token and channel ID:
```makefile
BOT_TOKEN="your_discord_bot_token"
CHANNEL_ID=your_discord_channel_id
```
5. **Run the Bot:** Execute the '**volleybot.py**' file to start the Bot:
```bash 
# Mac/Linux:
python3 volleybot.py
# Windows:
python volleybot.py
```