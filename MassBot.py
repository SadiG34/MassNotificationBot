import telebot

TOKEN = '##TOKEN'
bot = telebot.TeleBot(TOKEN)

GROUP_IDS = [##тут должны быть ID групп]

ALLOWED_USERS = [##админка]


def is_allowed(user_id):
    """Проверка, разрешен ли пользователь для выполнения команд."""
    return user_id in ALLOWED_USERS


@bot.message_handler(commands=['send'])
def send_message_to_groups(message):
    """Отправка сообщения в группы."""
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return

    msg_text = message.text[6:]

    if not msg_text.strip():
        bot.reply_to(message, "Пожалуйста, укажите текст сообщения для отправки.")
        return

    for group_id in GROUP_IDS:
        try:
            bot.send_message(group_id, msg_text)
        except Exception as e:
            print(f"Не удалось отправить сообщение в группу {group_id}: {e}")

    bot.reply_to(message, "Сообщение отправлено во все указанные группы.")


@bot.message_handler(commands=['addgroup'])
def add_group(message):
    """Добавление группы в список."""
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return

    group_id = message.text[10:].strip()

    if not group_id.isdigit():
        bot.reply_to(message, "Пожалуйста, укажите корректный ID группы.")
        return

    GROUP_IDS.append(int(group_id))
    bot.reply_to(message, f"Группа с ID {group_id} добавлена в список.")


@bot.message_handler(commands=['listgroups'])
def list_groups(message):
    """Вывод списка групп."""
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return

    if not GROUP_IDS:
        bot.reply_to(message, "Список групп пуст.")
    else:
        group_list = "\n".join(str(group_id) for group_id in GROUP_IDS)
        bot.reply_to(message, f"Список групп:\n{group_list}")


@bot.message_handler(commands=['removegroup'])
def remove_group(message):
    """Удаление группы из списка."""
    if not is_allowed(message.from_user.id):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return

    group_id = message.text[12:].strip()

    try:
        GROUP_IDS.remove(int(group_id))
        bot.reply_to(message, f"Группа с ID {group_id} удалена из списка.")
    except ValueError:
        bot.reply_to(message, f"Группа с ID {group_id} не найдена в списке.")


bot.polling(none_stop=True)

### Описание функций

# - /send <текст>: Отправляет указанное сообщение во все группы из вашего списка.
# - /addgroup : Добавляет указанную группу в список, если ID корректный.
# - /listgroups: Выводит список всех групп, в которые бот может отправлять сообщения.
# - /removegroup : Удаляет указанную группу из списка.
