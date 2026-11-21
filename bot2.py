import os
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp

BOT_TOKEN = "8961568562:AAH2J2o8LvPERKTZzPUcqsGWvGf9hchF6tc"


def download_video(url: str, output_dir: str) -> str:
  ydl_opts = {
      "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
      "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
      "noplaylist": True,
      "quiet": True,
  }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    return ydl.prepare_filename(info)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = (update.message.text or "").strip()
  if not text.startswith(("http://", "https://")):
    await update.message.reply_text("Send a valid video link.")
    return

  status_msg = await update.message.reply_text("Downloading video...")
  with tempfile.TemporaryDirectory() as tmpdir:
    try:
      file_path = download_video(text, tmpdir)
      await update.message.reply_video(video=open(file_path, "rb"))
    except Exception as e:
      await update.message.reply_text(f"Failed to download: {e}")
    finally:
      await status_msg.delete()


def main():
  app = ApplicationBuilder().token(BOT_TOKEN).build()
  app.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
  )
  app.run_polling()


if __name__ == "__main__":
  main()
