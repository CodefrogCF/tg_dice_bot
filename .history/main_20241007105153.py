import logging
import random
random.seed()
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler, filters)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define states
DICE_TYPE = range(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their preferred car type."""
    reply_keyboard = [['D6', 'D20']]

    await update.message.reply_text(
        '<b>Welcome to the PnP Dice Bot!\n'
        'Choose the Dice you need.</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return DICE_TYPE


async def dice_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's dice type."""
    user = update.message.from_user
    context.user_data['dice_type'] = update.message.text
    dice = {"D6", "D20"}
    logger.info('Dice type of %s: %s', user.first_name, update.message.text)
    await update.message.reply_text(
        f'<b>You selected the {update.message.text} dice.</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove(),
    )

'''
    # Define inline buttons for car color selection
    keyboard = [
        [InlineKeyboardButton('Red', callback_data='Red')],
        [InlineKeyboardButton('Blue', callback_data='Blue')],
        [InlineKeyboardButton('Black', callback_data='Black')],
        [InlineKeyboardButton('White', callback_data='White')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('<b>Please choose:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return CAR_COLOR
'''
'''
async def car_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the user's car color."""
    query = update.callback_query
    await query.answer()
    context.user_data['car_color'] = query.data
    await query.edit_message_text(
        text=f'<b>You selected {query.data} color.\n'
             f'Would you like to fill in the mileage for your car?</b>',
        parse_mode='HTML'
    )
'''
'''
    # Define inline buttons for mileage decision
    keyboard = [
        [InlineKeyboardButton('Fill', callback_data='Fill')],
        [InlineKeyboardButton('Skip', callback_data='Skip')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('<b>Choose an option:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return CAR_MILEAGE_DECISION
'''
'''
async def car_mileage_decision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user to fill in the mileage or skip."""
    query = update.callback_query
    await query.answer()
    decision = query.data

    if decision == 'Fill':
        await query.edit_message_text(text='<b>Please type in the mileage (e.g., 50000):</b>', parse_mode='HTML')
        return CAR_MILEAGE
    else:
        await query.edit_message_text(text='<b>Mileage step skipped.</b>', parse_mode='HTML')
        return await skip_mileage(update, context)
'''
'''
async def car_mileage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the car mileage."""
    context.user_data['car_mileage'] = update.message.text
    await update.message.reply_text('<b>Mileage noted.\n'
                                    'Please upload a photo of your car 📷, or send /skip.</b>',
                                    parse_mode='HTML')
    return PHOTO
'''
'''
async def skip_mileage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the mileage input."""
    context.user_data['car_mileage'] = 'Not provided'

    text = '<b>Please upload a photo of your car 📷, or send /skip.</b>'

    # Determine the correct way to send a reply based on the update type
    if update.callback_query:
        # If called from a callback query, use the callback_query's message
        chat_id = update.callback_query.message.chat_id
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        # Optionally, you might want to acknowledge the callback query
        await update.callback_query.answer()
    elif update.message:
        # If called from a direct message
        await update.message.reply_text(text)
    else:
        # Handle other cases or log an error/warning
        logger.warning('skip_mileage was called without a message or callback_query context.')

    return PHOTO
'''
'''
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo."""
    photo_file = await update.message.photo[-1].get_file()
    # Correctly store the file_id of the uploaded photo for later use
    context.user_data['car_photo'] = photo_file.file_id  # Preserve this line

    # Inform user and transition to summary
    await update.message.reply_text('<b>Photo uploaded successfully.\n'
                                    'Let\'s summarize your selections.</b>',
                                    parse_mode='HTML'
    )
    await summary(update, context)  # Proceed to summary
'''
'''
async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo upload."""
    await update.message.reply_text('<b>No photo uploaded.\n'
                                    'Let\'s summarize your selections.</b>',
                                    parse_mode='HTML')
    await summary(update, context)
'''
'''
async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Summarizes the user's selections and ends the conversation, including the uploaded image."""
    selections = context.user_data
    # Construct the summary text
    summary_text = (f"<b>Here's what you told me about your car:\n</b>"
                    f"<b>Car Type:</b> {selections.get('car_type')}\n"
                    f"<b>Color:</b> {selections.get('car_color')}\n"
                    f"<b>Mileage:</b> {selections.get('car_mileage')}\n"
                    f"<b>Photo:</b> {'Uploaded' if 'car_photo' in selections else 'Not provided'}")

    chat_id = update.effective_chat.id

    # If a photo was uploaded, send it back with the summary as the caption
    if 'car_photo' in selections and selections['car_photo'] != 'Not provided':
        await context.bot.send_photo(chat_id=chat_id, photo=selections['car_photo'], caption=summary_text, parse_mode='HTML')
    else:
        # If no photo was uploaded, just send the summary text
        await context.bot.send_message(chat_id=chat_id, text=summary_text, parse_mode='HTML')

    return ConversationHandler.END
'''

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
#            CAR_COLOR: [CallbackQueryHandler(car_color)],
#            CAR_MILEAGE_DECISION: [CallbackQueryHandler(car_mileage_decision)],
#            CAR_MILEAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, car_mileage)],
#            PHOTO: [
#                MessageHandler(filters.PHOTO, photo),
#                CommandHandler('skip', skip_photo)
#            ],
#            SUMMARY: [MessageHandler(filters.ALL, summary)]
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