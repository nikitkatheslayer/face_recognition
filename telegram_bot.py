import os
import telebot
import config_telebot
from face_detection import FaceDetector

detector = FaceDetector(config_telebot.face_cascade_path)

bot = telebot.TeleBot(config_telebot.TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    sti = open("sticker/5199625264102904058.tgs", "rb")
    bot.send_sticker(message.chat.id, sti)

    mess = f"<b>{message.from_user.first_name}</b>, отправь мне видео или фотографию, чтобы я распознал лицо"
    bot.send_message(message.chat.id, mess, parse_mode="html")

@bot.message_handler(content_types=["photo"])
def get_user_photo(message):

    bot.send_message(message.chat.id, "Идёт обработка изображения⏳", parse_mode="html")

    file_photo = bot.get_file(message.photo[-1].file_id)
    file_name, file_extension = os.path.splitext(file_photo.file_path)

    downloaded_file_photo = bot.download_file(file_photo.file_path)

    src = "image/" + message.photo[-1].file_id + file_extension
    with open(src, "wb") as new_file:
        new_file.write(downloaded_file_photo)

    detector.recognize_face(src)

    bot.send_message(message.chat.id, "Отправляю вам изображение...", parse_mode="html")
    detected_file_photo_path = "image/" + message.photo[-1].file_id + "_detected_faces.jpg"

    detected_file_photo = open(detected_file_photo_path, "rb")
    bot.send_photo(message.chat.id, detected_file_photo)

    bot.send_message(message.chat.id, "Можешь отправить еще что-нибудь", parse_mode="html")

@bot.message_handler(content_types=["video"])
def get_user_video(message):

    bot.send_message(message.chat.id, "Идёт обработка видео⏳", parse_mode="html")

    file_video = bot.get_file(message.video.file_id)
    file_name, file_extension = os.path.splitext(file_video.file_path)

    downloaded_file_video = bot.download_file(file_video.file_path)

    src = "video/" + file_video.file_id + file_extension
    with open(src, "wb") as new_file:
        new_file.write(downloaded_file_video)

    detector.recognize_video(src)

    bot.send_message(message.chat.id, "Отправляю вам видео...", parse_mode="html")
    detected_file_video_path = "video/" + file_video.file_id + "_detected_faces.mp4"

    detected_file_video = open(detected_file_video_path, "rb")
    bot.send_video(message.chat.id, detected_file_video)

    bot.send_message(message.chat.id, "Можешь отправить еще что-нибудь", parse_mode="html")

@bot.message_handler(content_types=["file", "text", "voice", "document"])
def handl_errors(message):
    bot.send_message(message.chat.id, "Отправьте фото или видео")

bot.polling(none_stop=True)