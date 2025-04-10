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
    reply_keyboard = [['D6', 'D20']]
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
        msg = "You rolled a:"
        dice = d6
    elif update.message.text.lower() == "d20":
        msg = "You rolled a:"
        dice = d20
    else:
        msg = "thats not"
        dice = "a dice"

    await update.message.reply_text(
        f"""<b>                 {update.message.text}\n
        {msg} {dice}</b>""",
        
        parse_mode='HTML',
    )
    print(dice)

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