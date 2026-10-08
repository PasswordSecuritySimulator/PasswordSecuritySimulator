  import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

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


# التوكن يُقرأ من Environment Variables في Render
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("لم يتم العثور على TOKEN في Environment Variables.")


# Web Server بسيط حتى يتعرف Render على الـ Port
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Password Security Simulator is running!")

    def log_message(self, format, *args):
        return


def run_web_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Web server is running on port {port}...")
    server.serve_forever()


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
    # تشغيل Web Server في الخلفية حتى Render لا يعتبر الخدمة متوقفة
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    # تشغيل البوت
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
