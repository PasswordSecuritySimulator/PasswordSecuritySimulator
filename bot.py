from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8908534809:AAH4Vx7PxwC2_BTO5_WRxri321slFA3qlLo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔐 أهلاً بك في Password Security Simulator!\n\n"
        "البوت يعمل بنجاح ✅"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot is running...")

app.run_polling()