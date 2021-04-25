import logging
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import settings
import functions


TOKEN = settings.API_KEY

PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}

commands = [
    "/start - начать диалог с колоботом",
    "/help - подсказка о том, как начать пользоваться ботом",
    "/count_sistem - функция для того, что переводить числа из одной системы счисления в другую",
    "/sequences_a - фунукция для того, чтобы расчитать сумму n первых членов арифметической прогрессии",
    "/sequences_g - функция для того, чтобы расчитать сумму n первых членов геометрической прогрессии",
    ""
]

for_cnt_sis = {
    "num": 0,
    "sis1": 0,
    "sis2": 0
}

for_seq = {
    "a1/b1": 0,
    "d/q": 0,
    "n": 0,
    "f": 0
}

reply_keyboard = [["арифметическая", "геометрическая"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

logging.basicConfig(filename="bot.log", level=logging.INFO)


def cnt_sis(update, context):
    update.message.reply_text("Я умею переводить целые положительные числа из одной системы счисления в другую легко "
                              "и просто! (я могу перевести любое целое положительное число в (2ой - 10ой) "
                              "системе счисления в любую другую (так же от 2ой до 10ой))")
    update.message.reply_text("Вам нужная моя помощь в этом?")
    if ("да" in update.message.text.lower() or "yes" in update.message.text.lower() or
        "of course" in update.message.text.lower() or "конечно" in update.message.text.lower()) \
            and ("не" not in update.message.text.lower() or "no" not in update.message.text.lower()):
        update.message.reply_text("Введите целое положительное число, которое хотите перевести:")
        return 1
    else:
        update.message.reply_text("Ну ладно, как пожелаете...")
        return ConversationHandler.END


def cnt_sis1(update, context):
    if not update.message.text.isdigit():
        update.message.reply_text("Введите, пожалйста, в правильном формате: любое целое положительное число")
        return 1
    if int(update.message.text) != float(update.message.text):
        update.message.reply_text("Введите, пожалйста, в правильном формате: любое целое положительное число")
        return 1
    if int(update.message.text) < 0:
        update.message.reply_text("Введите, пожалйста, в правильном формате: любое целое положительное число")
        return 1
    for_cnt_sis["num"] = int(update.message.text)
    update.message.reply_text("Теперь введите в какой системе считсления оно находится(целое число от 2 до 10)")
    return 2


def cnt_sis2(update, context):
    if not update.message.text.isdigit():
        update.message.reply_text("Введите, пожалйста, систему счисления в правильном формате: целое число от 2 до 10")
        return 2
    if int(update.message.text) != float(update.message.text):
        update.message.reply_text("Введите, пожалйста, систему счисления в правильном формате: целое число от 2 до 10")
        return 2
    if not (1 < int(update.message.text) < 11):
        update.message.reply_text("Введите, пожалйста, систему счисления в правильном формате: целое число от 2 до 10")
        return 2
    for_cnt_sis["sis1"] = int(update.message.text)
    update.message.reply_text("А теперь введите в какую систему счисления вы хотите его перевести")
    return 3


def cnt_sis3(update, context):
    if not update.message.text.isdigit():
        update.message.reply_text("Введите, пожалйста систему счисления в правильном формате: целое число от 2 до 10")
        return 3
    if int(update.message.text) != float(update.message.text):
        update.message.reply_text("Введите, пожалйста систему счисления в правильном формате: целое число от 2 до 10")
        return 3
    if not (1 < int(update.message.text) < 11):
        update.message.reply_text("Введите, пожалйста систему счисления в правильном формате: целое число от 2 до 10")
        return 3
    for_cnt_sis["sis2"] = int(update.message.text)
    update.message.reply_text(str(for_cnt_sis["num"]) + " в " + str(for_cnt_sis["sis1"]) +
                              "ой системе счисления равно " + functions.perevod(for_cnt_sis) + " в " +
                              str(for_cnt_sis["sis2"]) + "ой системе счисления")
    return ConversationHandler.END


def seq(update, context):
    update.message.reply_text("Могу посчитать сумму первых n членов геометрической прогрессии по её первому члену и"
                              " знаменателю прогрессии! Вам нужна моя помощь?")
    return 4


def seq4(update, context):
    if ("да" in update.message.text.lower() or "yes" in update.message.text.lower() or
        "of course" in update.message.text.lower() or "конечно" in update.message.text.lower()) \
            and ("не" not in update.message.text.lower() or "no" not in update.message.text.lower()):
        update.message.reply_text("А теперь выберите для какой прогрессии вы хотите посчитать сумму первых n членов",
                                  reply_markup=markup)
        return 5
    else:
        update.message.reply_text("Ну ладно, как пожелаете...")
        return ConversationHandler.END


def seq5(update, context):
    if update.message.text == "арифметическая":
        update.message.reply_text("Теперь введите первый член вашей арифметической прогрессии (число)")
        for_seq["f"] = 1
        return 1
    elif update.message.text == "геометрическая":
        update.message.reply_text("Теперь введите первый член вашей геометрической прогрессии (число)")
        for_seq["f"] = 0
        return 1
    else:
        update.message.reply_text("Я не понял, какую прогрессию вы выбрали, пожалуйста выберите ещё раз",
                                  reply_markup= markup)
        return 5


def seq1(update, context):
    if not update.message.text.isdigit():
        update.message.reply_text("Пожалуйста, введите первый член в правильном формате: число")
        return 1
    if for_seq["f"]:
        update.message.reply_text("А теперь введите разность вашей арифметической прогрессии(число)")
    else:
        update.message.reply_text("А теперь введите знаменатель вашей геометрической прогрессии(число)")
    return 2


def seq2(update, context):
    if not update.message.text.isdigit():
        if for_seq["f"]:
            update.message.reply_text("Пожалуйста, введите разность вашей арифметической прогрессии "
                                      "в правильном формате: число")
        else:
            update.message.reply_text("Пожалуйста, введите знаменатель вашей геометрической прогрессии "
                                      "в правильном формате: число")
        return 2
    if for_seq["f"]:
        update.message.reply_text("Ну и осталось ввести количесво членов в вашей фриметической прогрессии. "
                                  "Введите его(это должно быть целое неотрицательное число)")
    else:
        update.message.reply_text("Ну и осталось ввести количество членов в вашей геометрической прогрессии."
                                  "Введите его(это должно быть целое неотрицательное число)")
    return 3


def seq3(update, context):
    if not update.message.text.isdigit():
        update.message.reply_text("Пожалуйста, введите количество членов в правильном формате: "
                                  "целое неотрицательное ЧИСЛО")
    if int(update.message.text) != float(update.message.text):
        update.message.reply_text("Пожалуйста, введите количество членов в правильном формате: "
                                  "ЦЕЛОЕ неотрицательное число")
    if int(update.message.text) < 0:
        update.message.reply_text("Пожалуйста, введите количество членов в правильном формате: "
                                  "целое НЕОТРИЦАТЕЛЬНОЕ число")
    if for_seq["f"]:
        update.message.reply_text("Сумма первых " + str(for_seq["n"]) + " членов вашей арифметической прогресии равна "
                                  + str(functions.sequences(for_seq)))
    else:
        update.message.reply_text("Сумма первых " + str(for_seq["n"]) + " членов вашей геометрической прогресии равна "
                                  + str(functions.sequences(for_seq)))
    return ConversationHandler.END



def address(update, context):
    update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


def phone(update, context):
    update.message.reply_text("Телефон: +7(495)776-3030")


def site(update, context):
    update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


def work_time(update, context):
    update.message.reply_text("График работы: \n"
                              "пн: 8:00 - 18:00 \n"
                              "вт: 9:00 - 19:00 \n"
                              "ср: 8:30 - 18:30 \n"
                              "чт: 9:30 - 19:30 \n"
                              "пт: 9:00 - 18:00 \n"
                              "сб-вс: выходные дни")


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def echo(update, context):
    update.message.reply_text(update.message.text)


def cmd(update, context):
    cmds = commands[0]
    for x in commands[1:]:
        cmds += "\n"
        cmds += x
    update.message.reply_text(cmds)


def stop(update, context):
    update.message.reply_text("ОК")
    return ConversationHandler.END


def start(update, context):
    update.message.reply_text(
        "Привет! Я колобот. Я не малое умею")


def help(update, context):
    update.message.reply_text(
        "Если вам интересно узнать мои способности и функции, то напишите /commands, чтобы увидеть список моих команд")


def main():
    updater = Updater(TOKEN, use_context=True,
                      request_kwargs=PROXY)

    dp = updater.dispatcher

    count_sis = ConversationHandler(
        entry_points=[CommandHandler('count_sistem', cnt_sis)],

        states={

            1: [MessageHandler(Filters.text, cnt_sis1, pass_user_data=True)],

            2: [MessageHandler(Filters.text, cnt_sis2, pass_user_data=True)],

            3: [MessageHandler(Filters.text, cnt_sis3, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    sequences = ConversationHandler(
        entry_points=[CommandHandler('sequences', seq)],

        states={

            1: [MessageHandler(Filters.text, seq1, pass_user_data=True)],

            2: [MessageHandler(Filters.text, seq2, pass_user_data=True)],

            3: [MessageHandler(Filters.text, seq3, pass_user_data=True)],

            4: [MessageHandler(Filters.text, seq4, pass_user_data=True)],

            5: [MessageHandler(Filters.text, seq5, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(count_sis)
    dp.add_handler(sequences)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("commands", cmd))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("work_time", work_time))
    dp.add_handler(CommandHandler("close", close_keyboard))
    # dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()