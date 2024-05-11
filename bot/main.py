import logging
import re
import os
import paramiko

from db import DB
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext


load_dotenv()
TOKEN = os.getenv("TOKEN")
HOST = os.getenv('SSH_HOST')
PORT = os.getenv('SSH_PORT')
USERNAME = os.getenv('SSH_USER')
PASSWORD = os.getenv('SSH_PASSWORD')
allowed_commands = {'release': 'lsb_release -a',
                    'uname': 'uname -a',
                    'uptime': 'uptime',
                    'df': 'df -h',
                    'free': 'free --mega',
                    'mpstat': 'mpstat',
                    'w': 'w',
                    'auths': 'last -n 10',
                    'critical': 'journalctl -p crit | tail -n 5',
                    'ps': 'ps aux | head -n 50',
                    'ss': 'ss -tulnp',
                    'services': 'systemctl list-units --type=service --state=running'}



# Подключаем логирование
logging.basicConfig(
    filename='logfile.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
db = DB()


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')
    logger.info(f'User use /start')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')
    logger.info(f'User use /help')


def getEmails(update: Update, context):
    logger.info(f'User use /get_emails')
    output = db.executeCommand("SELECT * FROM emails;")
    update.message.reply_text(output)


def getPhones(update: Update, context):
    logger.info(f'User use /get_phone_numbers')
    output = db.executeCommand("SELECT * FROM phones;")
    update.message.reply_text(output)


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    logger.info(f'User use /find_phone_number')
    return 'findPhoneNumbers'


def insertPhonesINTOdb(update: Update, context):
    user_input = update.message.text.strip().lower()
    if user_input == 'нет':
        update.message.reply_text('Номера не были сохранены в БД')
        logger.info(f'User dont save phones in DB')
        return ConversationHandler.END

    elif user_input == 'да':
        phoneNumberList = context.user_data.get('phoneNumberList')
        command = "INSERT INTO phones (phone) VALUES "
        value_tuples = ", ".join([f"('{phone}')" for phone in phoneNumberList])
        command += value_tuples + ";"
        output = db.executeCommand(command)
        update.message.reply_text(output)
        return ConversationHandler.END

    else:
        update.message.reply_text('Напишите слово \'да\' или \'нет\'?')
        return 'insertPhonesINTOdb'


def findPhoneNumbers(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    logger.info(f'User send message with numbers')

    phoneNumRegex = re.compile(
        r"(8|\+7|7|\+8)[\s-]?(?:\(\d{3}\)|\d{3})[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
    )

    phoneNumberList = [match.group(0) for match in phoneNumRegex.finditer(user_input)]  # Ищем номера телефонов
    context.user_data['phoneNumberList'] = phoneNumberList

    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        logger.info(f'No numbers found in message')
        return ConversationHandler.END

    phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'  # Записываем очередной номер

    update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
    logger.info(f'Numbers found in message:\n{phoneNumbers}')

    update.message.reply_text('Сохранить найденные данные в БД(напишите слово \'да\' или \'нет\')?')
    return 'insertPhonesINTOdb'


def findEmailCommand(update: Update, context):
    logger.info(f'User use /find_email')
    update.message.reply_text('Введите текст для поиска emails: ')

    return 'findEmails'


def insertEmailsINTOdb(update: Update, context):
    user_input = update.message.text.strip().lower()
    if user_input == 'нет':
        update.message.reply_text('Emails не были сохранены в БД')
        logger.info(f'User dont save emails in DB')
        return ConversationHandler.END

    elif user_input == 'да':
        email_list = context.user_data.get('email_list')
        command = "INSERT INTO emails (email) VALUES "
        value_tuples = ", ".join([f"('{email}')" for email in email_list])
        command += value_tuples + ";"
        output = db.executeCommand(command)
        update.message.reply_text(output)
        return ConversationHandler.END

    else:
        update.message.reply_text('Напишите слово \'да\' или \'нет\'?')
        return 'insertEmailsINTOdb'


def findEmails(update: Update, context):
    user_input = update.message.text
    logger.info(f'User send message with emails')
    # Компилируем регулярное выражение для проверки email
    email_regex = re.compile(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    )
    email_list = [match.group(0) for match in email_regex.finditer(user_input)]
    context.user_data['email_list'] = email_list

    if not email_list:  # Обрабатываем случай, когда emails нет
        update.message.reply_text('Emails не найдены')
        logger.info(f'No emails found in message')
        return ConversationHandler.END

    emails = ''  # Создаем строку, в которую будем записывать emails
    for i in range(len(email_list)):
        emails += f'{i + 1}. {email_list[i]}\n'  # Записываем очередной email

    update.message.reply_text(emails)  # Отправляем сообщение пользователю
    update.message.reply_text('Сохранить найденные данные в БД(напишите слово \'да\' или \'нет\')?')
    return 'insertEmailsINTOdb'


def verifyPasswordCommand(update: Update, context):
    logger.info(f'User use /verify_password')
    update.message.reply_text('Введите пароль для проверки: ')

    return 'verifyPassword'


def verifyPassword(update: Update, context):
    user_input = update.message.text.strip()
    logger.info(f'User send message with password')
    # Компилируем регулярное выражение для проверки password
    password_regex = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()])[^\s]{8,}$"
    )

    message = ''
    if password_regex.match(user_input):
        message = "Пароль сложный."
        logger.info(f'User password is complex')
    else:
        message = "Пароль простой."
        logger.info(f'User password User password is easy')

    update.message.reply_text(message)  # Отправляем сообщение пользователю
    return ConversationHandler.END  # Завершаем работу обработчика диалога


def getOutput(command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Подключаемся к серверу
    ssh_client.connect(hostname=HOST, username=USERNAME, password=PASSWORD, port=int(PORT))

    # Выполняем команду
    stdin, stdout, stderr = ssh_client.exec_command(command)
    logger.info(f'User execute {command}')
    # Получаем результат
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    # Закрываем подключение
    ssh_client.close()

    return output, error


def execSomeOnRemote(update: Update, context):
    message_text = update.message.text.strip()
    if message_text.startswith('/get_'):
        # Извлекаем имя команды
        command = message_text[5:]
        if command in allowed_commands:

            logger.info(f'User use {message_text}')

            command = allowed_commands[command]

            output, error = getOutput(command)

            update.message.reply_text(f"Output:\n{output if output else error}")


def getAptListCommand(update: Update, context):
    logger.info(f'User use /get_apt_list')
    update.message.reply_text("Введите имя пакета или цифру '1' для получения списка всех пакетов.")
    return 'getAptList'


def getAptList(update: Update, context):
    user_input = update.message.text.strip()

    if user_input == "1":
        command = 'apt list --installed | head -n 50'
    else:
        command = f"apt list --installed | grep '^{user_input}'"
    output, error = getOutput(command)

    update.message.reply_text(f"Output:\n{output if output else error}")
    return ConversationHandler.END


def getReplLogs(update: Update, context):
    logger.info(f'User use /get_repl_logs')
    files = []
    text = ''
    try:
        # Перебираем все элементы в директории
        for entry in os.listdir('pg_data/logs'):
            # Соединяем путь директории с именем файла или папки
            full_path = os.path.join('pg_data/logs', entry)
            # Проверяем, является ли элемент файлом
            if os.path.isfile(full_path):
                files.append(entry)
    except Exception as e:
        update.message.reply_text(text)
        logger.info(e)
        return

    for filename in files:
        try:
            with open(f'pg_data/logs/{filename}', 'r') as file:
                for line in file:
                    if 'replication' in line:
                        text += line + '\n'
        except Exception as e:
            text = e
    logger.info(f'User get logs')
    update.message.reply_text(text)


def main():

    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'insertPhonesINTOdb': [MessageHandler(Filters.text & ~Filters.command, insertPhonesINTOdb)],
        },
        fallbacks=[]
    )

    # Обработчик диалога
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            'insertEmailsINTOdb': [MessageHandler(Filters.text & ~Filters.command, insertEmailsINTOdb)],
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )

    convHandlerAPTlist = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptListCommand)],
        states={
            'getAptList': [MessageHandler(Filters.text & ~Filters.command, getAptList)],
        },
        fallbacks=[]
    )


    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(convHandlerAPTlist)
    dp.add_handler(MessageHandler(Filters.regex(r'^/get_(?!apt_list|emails|phone_numbers|repl_logs).*'), execSomeOnRemote))
    dp.add_handler(CommandHandler("get_emails", getEmails))
    dp.add_handler(CommandHandler("get_phone_numbers", getPhones))
    dp.add_handler(CommandHandler("get_repl_logs", getReplLogs))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
