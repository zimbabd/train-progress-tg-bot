from telebot import types
from datetime import datetime
import os
from utils.pdf_generator import generate_statistics_pdf
from repository.training_sessions_repository import TrainingSessionsRepository
from config import DB_PATH

# Initializing the repository for working with training sessions
training_repo = TrainingSessionsRepository(str(DB_PATH))

def show_statistics_options(bot, message):
    """Shows buttons for selecting statistics."""
    markup = types.InlineKeyboardMarkup()
    last_5_button = types.InlineKeyboardButton("Last 5 workouts", callback_data="last_5")
    full_stats_button = types.InlineKeyboardButton("All statistics in PDF", callback_data="full_stats")

    markup.add(last_5_button, full_stats_button)
    bot.send_message(message.chat.id, "Select statistics type:", reply_markup=markup)


def show_last_5_sessions(call, bot):
    """Shows the user's last 5 workouts."""
    user_id = call.from_user.id  # Get the user ID
    sessions = training_repo.get_last_sessions_by_user_id(user_id)  # Get the user's last 5 workouts

    if not sessions:
        bot.send_message(call.message.chat.id, "You don't have any training yet.")
        return

    # We create a message with the last 5 workouts
    stats_message = "Your last 5 workouts:\n\n"
    for session in sessions:
        template_name = session[1]
        session_date_str = session[3]

        try:
            session_date = datetime.strptime(session_date_str, "%Y-%m-%d %H:%M:%S.%f")
            formatted_date = session_date.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            formatted_date = "Date not available"  # If there is an error parsing the date

        # Let's start generating a message for one workout
        session_message = f"Training: {template_name}\n"

        # Check and add only those parameters that are filled in
        if session[4]:  # distance
            session_message += f"Distance: {session[4]} km\n"
        if session[5]:  # tempo
            session_message += f"Tempo: {session[5]} km/h\n"
        if session[6]:  # pulse
            session_message += f"Pulse: {session[6]} beats/min\n"
        if session[7]:  # quantity
            session_message += f"Quantity: {session[7]}\n"
        if session[8]:  # sets
            session_message += f"Sets: {session[8]}\n"
        if session[9]:  # weight
            session_message += f"Weight: {session[9]} kg\n"

        # Add date
        session_message += f"Date: {formatted_date}\n"
        session_message += "---------------------------\n"

        # Add a session message to the general statistics text
        stats_message += session_message

    # Send a message to the user
    bot.send_message(call.message.chat.id, stats_message)

def send_full_statistics_pdf(call, bot):
    """Sends a PDF with all user statistics."""
    user_id = call.from_user.id  # Get the user ID
    sessions = training_repo.get_all_sessions_by_user_id(user_id)  # Get all session data
    if not sessions:
        bot.send_message(call.message.chat.id, "You don't have any training yet.")
        return
    # Generate the PDF using the sessions and user ID.
    pdf_path = generate_statistics_pdf(sessions, user_id)

    # Send PDF to user
    with open(pdf_path, 'rb') as pdf_file:
        bot.send_document(call.message.chat.id, pdf_file)

    # Delete PDF after sending
    os.remove(pdf_path)
