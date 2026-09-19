from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "ضع _التوكن _هنا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔐 أهلاً بك في Password Security Simulator!\n\n"
        "البوت يعمل بنجاح ✅"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot is running...")

app.run_polling()
