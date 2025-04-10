import logging
import random

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters, CallbackContext)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

async def start(update: Update, context) -> None:
    # Definiere die Tasten des Reply-Keyboards für 3-, 6- und 20-seitigen Würfel
    reply_keyboard = [['D3', 'D6', 'D20', '3xD20', 'Bodypart']]
    
    # Erstelle das Keyboard mit der Option, es dauerhaft anzuzeigen
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    
    # Sende die Begrüßungsnachricht und füge das Keyboard hinzu
    await update.message.reply_text(
        'Hi there! Tap a Button to roll',
        reply_markup=markup
    )

# Funktion für den 3-Seitigen Würfel
async def wuerfeln_3(update: Update, context) -> None:
    zahl = random.randint(1, 3) # Zufallszahl zwischen 1 und 3
    await update.message.reply_text(f"""<b> You rolled a:\n
         {zahl}</b>""", parse_mode='HTML')

# Funktion für den 6-seitigen Würfel
async def wuerfeln_6(update: Update, context) -> None:
    zahl = random.randint(1, 6) # Zufallszahl zwischen 1 und 6
    await update.message.reply_text(f"""<b> You rolled a:\n
         {zahl}</b>""", parse_mode='HTML')

# Funktion für den 20-seitigen Würfel
async def wuerfeln_20(update: Update, context) -> None:
    zahl = random.randint(1, 20)  # Zufallszahl zwischen 1 und 20
    await update.message.reply_text(f"""<b> You rolled a:\n
        {zahl}</b>""", parse_mode='HTML')

# Funktion für 3 20-seitige Würfel
async def wuerfeln_3x20(update: Update, context) -> None:
    zahl1 = random.randint(1, 20)  # Zufallszahl 1 zwischen 1 und 20
    zahl2 = random.randint(1, 20)  # Zufallszahl 2 zwischen 1 und 20
    zahl3 = random.randint(1, 20)  # Zufallszahl 3 zwischen 1 und 20
    await update.message.reply_text(
        f"""<b>You rolled:\n
  {zahl1}, {zahl2}, {zahl3}</b>""", parse_mode='HTML')

# Funktion für Körperteile
async def wuerfeln_koerperteil(update: Update, context) -> None:
#    kopf = 1
#    koerper = 2
#    arme = 3
#    beine = 4
    koerperteil = random.randint(1, 4)
    if koerperteil == 1:
        await update.message.reply_text(
        f"""<b>You hit the\n
    Head</b>""", parse_mode='HTML')
    if koerperteil == 2:
        await update.message.reply_text(
        f"""<b>You hit the\n
    Body</b>""", parse_mode='HTML')
    if koerperteil == 3:
        await update.message.reply_text(
        f"""<b>You hit the\n
    Arm</b>""", parse_mode='HTML')
    koerperteil = random.randint(1, 4)
    if koerperteil == 4:
        await update.message.reply_text(
        f"""<b>You hit the\n
    Leg</b>""", parse_mode='HTML')

# Funktion, die Textnachrichten verarbeitet
async def echo(update: Update, context) -> None:
    # Überprüfe, ob der Benutzer einen der Würfel gedrückt hat
    if update.message.text == "D3":
        await wuerfeln_3(update, context)
    elif update.message.text == "D6":
        await wuerfeln_6(update, context)
    elif update.message.text == "D20":
        await wuerfeln_20(update, context)
    elif update.message.text == "3xD20":
        await wuerfeln_3x20(update, context)
    elif update.message.text == "Bodypart":
        await wuerfeln_koerperteil(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    application = Application.builder().token("7797876392:AAHiQilMfUx28YTJPBrGgANmTVVtsgNhXzc").build()

    application.add_handler(CommandHandler("start", start))
    
    # Nachrichten-Handler, um auf Textnachrichten wie "D6" oder "D20" zu reagieren
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.add_handler(CommandHandler('stop', cancel)),

    application.run_polling()


if __name__ == '__main__':
    main()