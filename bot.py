import os, subprocess
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = os.environ.get("TOKEN")
bot = Bot(TOKEN)
app = Flask(__name__)

CONFIG = "first-order-model/config/vox-256.yaml"
CHECKPOINT = "first-order-model/vox-cpk.pth"
DRIVING_VIDEO = "first-order-model/sup-mat/driving.mp4"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp = Dispatcher(bot, None, use_context=True)

    def start(update, context):
        update.message.reply_text("Hola! Envíame una foto y la animaré 🚀")

    def handle_photo(update, context):
        photo = update.message.photo[-1]
        file_id = photo.file_id
        file = bot.get_file(file_id)
        os.makedirs("downloads", exist_ok=True)
        img_path = f"downloads/{file_id}.jpg"
        result_video = f"downloads/{file_id}_result.mp4"
        file.download(img_path)

        subprocess.run([
            "python", "first-order-model/demo.py",
            "--config", CONFIG,
            "--checkpoint", CHECKPOINT,
            "--source_image", img_path,
            "--driving_video", DRIVING_VIDEO,
            "--result_video", result_video
        ])

        if os.path.exists(result_video):
            with open(result_video, "rb") as f:
                context.bot.send_video(chat_id=update.message.chat_id, video=f)
        else:
            update.message.reply_text("Error al generar el video 😢")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot corriendo 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
