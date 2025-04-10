import logging
import random

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define states
DICE_TYPE = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their preferred dice type."""
    while True:
        reply_keyboard = [['D6', 'D20', "EXIT"]]
        await update.message.reply_text(
            '<b>Welcome to the PnP Dice Bot!\n'
            'Choose the Dice you need.</b>',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
        )

        return DICE_TYPE

async def dice_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    random.seed()
    d6 = random.randint(1, 6)
    d20 = random.randint(1, 20)
    """Stores the user's dice type."""
    user = update.message.from_user
    context.user_data['dice_type'] = update.message.text
    dice = 0
    logger.info('Dice type of %s: %s', user.first_name, update.message.text)

    if update.message.text.lower() == "d6":
        dice = d6
    else:
        dice = d20

    await update.message.reply_text(
        f"""<b>You selected the {update.message.text} dice.\n
                {dice}
        </b>""",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove(),
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    application = Application.builder().token("7797876392:AAHiQilMfUx28YTJPBrGgANmTVVtsgNhXzc").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DICE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, dice_type)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Handle the case when a user sends /start but they're not in a conversation
    application.add_handler(CommandHandler('start', start))

    application.run_polling()


if __name__ == '__main__':
    main()

'''
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def reply(update, context):
    await update.message.reply_text("Hello there!")

def main():
    """
    Handles the initial launch of the program (entry point).
    """
    token = "7797876392:AAHiQilMfUx28YTJPBrGgANmTVVtsgNhXzc"
    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
    application.add_handler(MessageHandler(filters.TEXT, reply))
    application.add_handler(CommandHandler("hello", reply)) # new command handler here
    print("Telegram Bot started!", flush=True)
    application.run_polling()

if __name__ == '__main__':
    main()
'''