from telegram.ext import Application


def main():
    """
    Handles the initial launch of the program (entry point).
    """
    token = "7797876392:AAHiQilMfUx28YTJPBrGgANmTVVtsgNhXzc"
    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
    print("Telegram Bot started!", flush=True)
    application.run_polling()


if __name__ == '__main__':
    main()