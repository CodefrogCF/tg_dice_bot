import logging
import random

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters, CallbackContext)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

async def start(update: Update, context) -> None:
    # define buttons of the Reply-Keyboard
    reply_keyboard = [['D3', 'D6', 'D20', '3xD20', 'Bodypart']]
    
    # create a Keyboard with the option, to view it all the time
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    
    # Send first message and add the keyboard
    await update.message.reply_text(
        'Hi there! Tap a Button to roll',
        reply_markup=markup)

# function for d3
async def random_3(update: Update, context) -> None:
    dice = random.randint(1, 3)
    await update.message.reply_text(f"""<b> You rolled a:\n
         {dice}</b>""", parse_mode='HTML')

# function for d6
async def random_6(update: Update, context) -> None:
    dice = random.randint(1, 6)
    await update.message.reply_text(f"""<b> You rolled a:\n
         {dice}</b>""", parse_mode='HTML')

# function for d20
async def random_20(update: Update, context) -> None:
    dice = random.randint(1, 20)
    await update.message.reply_text(f"""<b> You rolled a:\n
        {dice}</b>""", parse_mode='HTML')

# function for three d20s
async def random_3x20(update: Update, context) -> None:
    dice1 = random.randint(1, 20)
    dice2 = random.randint(1, 20)
    dice3 = random.randint(1, 20)
    await update.message.reply_text(f"""<b>You rolled:\n
  {dice1}, {dice2}, {dice3}</b>""", parse_mode='HTML')

# function for random bodypart
async def random_bodypart(update: Update, context) -> None:
    bodypart = random.randint(1, 4)
    if bodypart == 1:
        await update.message.reply_text("<b>You hit the\n\n    Head</b>", parse_mode='HTML')
    elif bodypart == 2:
        await update.message.reply_text("<b>You hit the\n\n    Body</b>", parse_mode='HTML')
    elif bodypart == 3:
        await update.message.reply_text("<b>You hit the\n\n    Arm</b>", parse_mode='HTML')
    elif bodypart == 4:
        await update.message.reply_text("<b>You hit the\n\n    Leg</b>", parse_mode='HTML')

# function to parse text-input
async def echo(update: Update, context) -> None:
    # check, if user pressed a dice-button
    if update.message.text == "D3":
        await random_3(update, context)
    elif update.message.text == "D6":
        await random_6(update, context)
    elif update.message.text == "D20":
        await random_20(update, context)
    elif update.message.text == "3xD20":
        await random_3x20(update, context)
    elif update.message.text == "Bodypart":
        await random_bodypart(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Cancels and ends the conversation.
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    # Run the bot.
    application = Application.builder().token("<YOUR TOKEN>").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("d3".lower(), random_3))
    application.add_handler(CommandHandler("d6".lower(), random_6))
    application.add_handler(CommandHandler("d20".lower(), random_20))
    application.add_handler(CommandHandler("d3x20".lower(), random_3x20))
    application.add_handler(CommandHandler("bodypart".lower(), random_bodypart))

    # message-handler, to react to text-messages as "D6" or "D20"
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.add_handler(CommandHandler("stop", cancel)),

    application.run_polling()


if __name__ == '__main__':
    main()


