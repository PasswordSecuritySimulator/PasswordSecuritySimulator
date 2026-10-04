from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from password_strength import evaluate_password
from security_tips import security_policy, security_tips
from malicious_code_analyzer import analyze_code
from url_checker import check_url

TOKEN = "ضع_التوكن_هنا"


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🔐 فحص كلمة المرور", callback_data="password"),
            InlineKeyboardButton("🌐 فحص الرابط", callback_data="url"),
        ],
        [
            InlineKeyboardButton("💻 فحص الكود", callback_data="code"),
            InlineKeyboardButton("🛡️ سياسة الأمان", callback_data="policy"),
        ],
        [InlineKeyboardButton("💡 نصائح أمنية", callback_data="tips")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = None
    await update.message.reply_text(
        "🔐 أهلاً بك في Password Security Simulator!\n\n"
        "اختر الخدمة التي تريد استخدامها:",
        reply_markup=main_menu(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "password":
        context.user_data["mode"] = "password"
        await query.message.reply_text("🔐 أرسل كلمة المرور لفحص قوتها.")

    elif query.data == "url":
        context.user_data["mode"] = "url"
        await query.message.reply_text("🌐 أرسل الرابط الذي تريد فحصه.")

    elif query.data == "code":
        context.user_data["mode"] = "code"
        await query.message.reply_text("💻 أرسل الكود البرمجي لتحليله.")

    elif query.data == "policy":
        context.user_data["mode"] = None
        await query.message.reply_text(security_policy())

    elif query.data == "tips":
        context.user_data["mode"] = None
        await query.message.reply_text(security_tips())


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")

    if mode == "password":
        await update.message.reply_text(str(evaluate_password(text)))
    elif mode == "url":
        await update.message.reply_text(check_url(text))
    elif mode == "code":
        await update.message.reply_text(str(analyze_code(text)))
    else:
        await update.message.reply_text(
            "اختر خدمة من القائمة:",
            reply_markup=main_menu(),
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
