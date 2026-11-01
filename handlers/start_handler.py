from model.user_model import User
from repository.user_repository import UserRepository
from telebot import types
from config import DB_PATH

user_repo = UserRepository(str(DB_PATH))

def handle_start(bot, message, reply_markup=None):

    user_id = message.from_user.id  # Get the user ID from the message

    # Check if the user is in the database
    existing_user = user_repo.get_user(user_id)
    if not existing_user:
        # If there is no user, create a new account
        first_name = message.from_user.first_name or "User"
        username = message.from_user.username or "Without a name"

        # Create a new user account
        user = User(user_id, username, first_name)
        user_repo.add_user(user)

    greeting = (
        "Welcome back!"
        if existing_user
        else f"Welcome, {message.from_user.first_name or 'there'}!"
    )
    bot.send_message(message.chat.id, greeting, reply_markup=reply_markup)
