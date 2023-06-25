import os
import logging
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store the streak count and start date
streak_count = 0
start_date = None

# Command handler for /start
def start(update, context):
    global streak_count, start_date
    update.message.reply_text('Welcome to the NoFap Streak Tracker Bot! Your current streak count is {}.'.format(streak_count))
    if start_date:
        update.message.reply_text('You started your streak on {}.'.format(start_date.strftime('%d/%m/%Y')))

# Command handler for /relapse
def relapse(update, context):
    global streak_count, start_date
    streak_count = 0
    start_date = None
    update.message.reply_text('Your streak count has been reset to 0.')

# Command handler for /setstreak
def set_streak(update, context):
    update.message.reply_text('Please provide the start date of your streak in the format dd/mm/yyyy.')
    # Set a handler to handle the user's reply
    context.user_data['waiting_for_date'] = True

def set_streak_date(update, context):
    global start_date
    if 'waiting_for_date' in context.user_data and context.user_data['waiting_for_date']:
        date_str = update.message.text
        try:
            start_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            update.message.reply_text(f'Streak start date set to: {start_date.strftime("%d/%m/%Y")}')
        except ValueError:
            update.message.reply_text('Invalid date format. Please use dd/mm/yyyy.')

        # Reset the flag
        context.user_data['waiting_for_date'] = False

# Command handler for /stats
def stats(update, context):
    global streak_count, start_date
    if streak_count > 0:
        update.message.reply_text('Your current streak count is {}. You started your streak on {}.'.format(streak_count, start_date.strftime('%d/%m/%Y')))
    else:
        update.message.reply_text('You have no current streak.')

# Message handler for all other commands
def unknown_command(update, context):
    update.message.reply_text('Invalid command. Please use /start to get your current streak count.')

# Main function
def main():
    # Get the bot token from the environment variable
    token = os.getenv('BOT_TOKEN')

    # Create the Updater
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("relapse", relapse))
    dp.add_handler(CommandHandler("setstreak", set_streak))
    dp.add_handler(CommandHandler("stats", stats))

    # Register the unknown command handler for all other commands
    dp.add_handler(MessageHandler(Filters.command, unknown_command))

    # Register the message handler for setting the streak date
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), set_streak_date))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
