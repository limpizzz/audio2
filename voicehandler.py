import requests
from config import iam, folder_id, token
from data import update_user_seconds, check_limit


def handle_voice_message(message, bot):
    user_id = message.from_user.id
    if message.voice is None:
        bot.send_message(message.chat.id, "отправь гс;)")
        return

    if not check_limit(user_id, message.voice.duration):
        bot.send_message(message.chat.id, "прости,лимит по времени превышен((")
        return

    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(f'https://api.telegram.org/file/bot{token}/{file_info.file_path}')

    duration = message.voice.duration
    if not update_user_seconds(user_id, duration):
        bot.send_message(message.chat.id, "гс слишком длинное и не будет обработано(.")
        return

    response = requests.post(
        'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize',
        headers={'Authorization': 'Bearer ' + iam},
        params={'folderId': folder_id},
        data=file.content
    )

    if response.status_code != 200:
        bot.send_message(message.chat.id, "Ошибка обработки голосового сообщения.")
        return

    bot.send_message(message.chat.id, response.json().get('result', "не удалось распознать гс."))
