import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "6341875224:AAFH19Td8nvWoOfQNkH2l9dfl9hvNyViZ80"   # ← توکن رباتت را اینجا بگذار

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک مستقیم ویدیو (.mp4) را بفرست تا برات دانلود کنم.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.endswith(".mp4"):
        await update.message.reply_text("این لینک mp4 مستقیم نیست. فقط لینک‌های مستقیم ویدیو پشتیبانی می‌شود.")
        return

    await update.message.reply_text("در حال دانلود از سرور… ⏳")

    try:
        filename = "video.mp4"
        
        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

        await update.message.reply_video(video=open(filename, "rb"), caption="ویدیو دانلود شد ✔️")
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"خطا در دانلود ❌\n{str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    app.run_polling()   # ← بدون async

if __name__ == "__main__":
    main()              # ← بدون asyncio.run()
