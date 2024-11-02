# NotifyMe Bot
<img src="https://github.com/oleksharh/Notify-Me-Bot/blob/main/assets/notify-me-bot-avatar.jpg" alt="Bot Profile Picture" width="200" />

**NotifyMe Bot** is a simple Telegram reminder bot designed to keep you on track with persistent notifications. Simply type your reminder message, and a menu will guide you to set up the task as you like. The bot will continue reminding you until you mark the task as completed.

### Features
- **Quick Task Creation:** Type in your message, and the bot’s menu helps you set up your reminder effortlessly.
- **Persistent Reminders:** Reminders keep coming until each task is completed.
- **Task Management Commands:** 
  - **/manage** – Update or delete tasks easily.
  - **/list** – View all active tasks and reminders at a glance.
- **Priority-based Reminders:** Set reminders from `low` (morning only) to `ultra` (hourly) to fit your schedule (currently only up to high priority (sends reminders at 10, 15, 20)).

> **Try it out!** The bot is live on Telegram. Start managing your tasks with [@notifyy_mebot](https://t.me/notifyy_mebot).

### Warning
> **Currently in Development:** Please note that the database may be wiped out during updates, which means your tasks could be permanently deleted. Feel free to experiment with the bot, fork the repository, or use this bot's structure as a template for your own projects!


### Usage
1. **Add a Task:** Type your reminder message, then choose from the menu options to customize it.
2. **Manage Tasks:** Use `/manage` to update or delete tasks.
3. **List All Tasks:** Use `/list` to see all your tasks and reminders.
4. **Complete a Task:** Mark tasks as done directly from reminders to stop notifications.

### Installation and Hosting
The bot is currently hosted, but if you’d like to host it yourself or modify its functionality:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/<username>/NotifyMe-Bot.git
    cd NotifyMe-Bot
    ```
2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Set Up Environment Variables:**
   - Create a `.env` file and add your bot token from [BotFather](https://core.telegram.org/bots#botfather).
    ```
    TELEGRAM_BOT_TOKEN=your_bot_token_here
    MONGODB_URI=your_mongoDB_URI
    DATABASE_NAME=your_db_name
    EXEMPT_USER_IDS=user_ids that have no limitations
    ```
4. **Run the Bot:**
    ```bash
    python bot.py
    ```

### Tech Stack
- **Telegram API**: For seamless user interaction.
- **Python**: Bot logic and task management.
- **Aiogram**: Python framework optimized for Telegram bots.
- **MongoDB**: Database for task storage and reminder configurations.

### Notes
> **Currently in Development:** Please note that the database may be wiped out during updates, which means your tasks could be permanently deleted. Feel free to experiment with the bot, fork the repository, or use this bot's structure as a template for your own projects!

### License
This project is open-source and available under the MIT License.
