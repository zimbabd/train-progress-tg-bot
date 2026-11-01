import datetime
from telebot import types


def handle_run(bot, call, exercise_repo, training_repo):
    """
    Function for processing the 'running' exercise.
    """
   # Get the exercise ID
    template_id = int(call.data.split('_')[-1])

    # Get the exercise template by ID (in this case running)
    template = exercise_repo.get_template_by_id(template_id)

    if template and template['template_name'] == 'run':
        # If the pattern is found and it's "run", we start querying the parameters
        bot.send_message(call.message.chat.id, "Enter the distance you ran (in km):")
        bot.register_next_step_handler(call.message,
                                       lambda m: process_distance(m, bot, exercise_repo, training_repo, template_id))
    else:
        bot.send_message(call.message.chat.id, "Error: Exercise not found.")


def process_distance(message, bot, exercise_repo, training_repo, template_id):
    # Get the distance
    try:
        distance = float(message.text)  # Convert to floating point number
        if distance <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for distance.")
        bot.register_next_step_handler(message,
                                       lambda m: process_distance(m, bot, exercise_repo, training_repo, template_id))
        return

    bot.send_message(message.chat.id, "Enter your running pace (in km/h):")

   # Register the next step to get the tempo
    bot.register_next_step_handler(message,
                                   lambda m: process_pace(m, bot, exercise_repo, training_repo, template_id, distance))


def process_pace(message, bot, exercise_repo, training_repo, template_id, distance):
    # Get the tempo
    try:
        pace = float(message.text)  # Convert to floating point number
        if pace <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for tempo.")
        bot.register_next_step_handler(message,
                                       lambda m: process_pace(m, bot, exercise_repo, training_repo, template_id, distance))
        return

    bot.send_message(message.chat.id, "Enter heart rate:")

    # Registering the next step to obtain the pulse
    bot.register_next_step_handler(message,
                                   lambda m: process_pulse(m, bot, exercise_repo, training_repo, template_id, distance,
                                                           pace))


def process_pulse(message, bot, exercise_repo, training_repo, template_id, distance, pace):
    # Getting the pulse
    try:
        pulse = int(message.text)  # Convert to integer
        if pulse <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for heart rate.")
        bot.register_next_step_handler(message,
                                       lambda m: process_pulse(m, bot, exercise_repo, training_repo, template_id, distance,
                                                                pace))
        return

    user_id = message.from_user.id  # Getting the user ID

    # Saving the training session in the database
    training_repo.add_training_session(
        user_id=user_id,
        template_id=template_id,
        distance=distance,
        pace=pace,
        pulse=pulse,
        session_date=datetime.datetime.now()
    )

   # Notify the user that the data was successfully written
    bot.send_message(message.chat.id, "Running workout successfully saved!")
