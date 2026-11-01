import telebot
from telebot import types
from handlers.start_handler import handle_start, user_repo
from handlers.training_program_handler import handle_training_program, handle_exercise_selection
from handlers.statistics_handler import show_statistics_options, show_last_5_sessions, send_full_statistics_pdf
from config import TOKEN_FILE

try:
    API_KEY = TOKEN_FILE.read_text(encoding="utf-8").strip()
except FileNotFoundError as exc:
    raise RuntimeError(f"Bot token file not found: {TOKEN_FILE}") from exc
if not API_KEY:
    raise RuntimeError(f"Bot token file is empty: {TOKEN_FILE}")
bot = telebot.TeleBot(API_KEY)

# Build the persistent reply keyboard.
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton('🏠 Main menu')
    btn_statistics = types.KeyboardButton('📊 Statistics')
    btn_support = types.KeyboardButton('💬 Support')
    btn_training = types.KeyboardButton('🏋️ Workout')

    markup.add(btn_start, btn_statistics)
    markup.add(btn_support, btn_training)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    markup = create_main_menu()
    existing_user = user_repo.get_user(message.from_user.id)
    if existing_user:
        bot.send_message(message.chat.id, "Welcome back!", reply_markup=markup)
    else:
        handle_start(bot, message, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🏠 Main menu')
def main_menu(message):
    start(message)


@bot.message_handler(commands=['statistics'])
def show_statistics_options_handler(message):
    show_statistics_options(bot, message)


@bot.message_handler(func=lambda message: message.text == '📊 Statistics')
def show_statistics_button(message):
    show_statistics_options(bot, message)


@bot.callback_query_handler(func=lambda call: call.data == "last_5")
def show_last_5_sessions_handler(call):
    show_last_5_sessions(call, bot)


@bot.callback_query_handler(func=lambda call: call.data == "full_stats")
def send_full_statistics_pdf_handler(call):
    send_full_statistics_pdf(call, bot)


@bot.message_handler(commands=['support'])
def support(message):
    bot.send_message(message.chat.id, "For any questions write @admin!")


@bot.message_handler(func=lambda message: message.text == '💬 Support')
def support_button(message):
    support(message)

# Handle the training command.
@bot.message_handler(commands=['training'])
def training(message):
    handle_training_program(bot, message)


@bot.message_handler(func=lambda message: message.text == '🏋️ Workout')
def training_button(message):
    training(message)

# Handle exercise selection callbacks.
@bot.callback_query_handler(func=lambda call: call.data.startswith('exercise_'))
def callback_handler(call):
    try:
        handle_exercise_selection(call, bot)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error has occurred: {str(e)}")


# Start long polling when run as a script.
if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
