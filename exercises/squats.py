import datetime
from telebot import types


def handle_squats(bot, call, exercise_repo, training_repo):
    """
    Function for processing the "squat" exercise.
    """
    # Get the exercise ID
    template_id = int(call.data.split('_')[-1])

   # Get an exercise template by ID (in this case squats)
    template = exercise_repo.get_template_by_id(template_id)

    if template and template['template_name'] == 'squats':
        # If a pattern is found and it's "squats", we start asking for parameters
        bot.send_message(call.message.chat.id, "Enter the number of squats:")
        bot.register_next_step_handler(call.message,
                                       lambda m: process_reps(m, bot, exercise_repo, training_repo, template_id))
    else:
        bot.send_message(call.message.chat.id, "Error: Exercise not found.")


def process_reps(message, bot, exercise_repo, training_repo, template_id):
    # Get the number of repetitions
    try:
        reps = int(message.text)
        if reps <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for repetitions.")
        bot.register_next_step_handler(message,
                                       lambda m: process_reps(m, bot, exercise_repo, training_repo, template_id))
        return

    bot.send_message(message.chat.id, "Enter the number of sets:")

    # Register the next step to get the number of sets
    bot.register_next_step_handler(message,
                                   lambda m: process_sets(m, bot, exercise_repo, training_repo, template_id, reps))


def process_sets(message, bot, exercise_repo, training_repo, template_id, reps):
    # We get the number of sets
    try:
        sets = int(message.text)
        if sets <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for sets.")
        bot.register_next_step_handler(message,
                                       lambda m: process_sets(m, bot, exercise_repo, training_repo, template_id, reps))
        return

    bot.send_message(message.chat.id, "Enter weight (in kg if available, otherwise leave blank):")

    # Registering the next step to get the weight
    bot.register_next_step_handler(message,
                                   lambda m: process_weight(m, bot, exercise_repo, training_repo, template_id, reps,
                                                            sets))


def process_weight(message, bot, exercise_repo, training_repo, template_id, reps, sets):
    # We get the weight
    weight = message.text.strip()
    if weight and not weight.isdigit():
        bot.send_message(message.chat.id, "Error: Please enter a valid value for weight.")
        bot.register_next_step_handler(message,
                                       lambda m: process_weight(m, bot, exercise_repo, training_repo, template_id, reps,
                                                                sets))
        return

    weight = float(weight) if weight else None  # If weight is not specified, save as None
    user_id = message.from_user.id # Get the user ID

    # Saving the training session in the database
    training_repo.add_training_session(
        user_id=user_id,
        template_id=template_id,
        quantity=reps,
        sets=sets,
        weight=weight,
        session_date=datetime.datetime.now()
    )

    # Notify the user that the data was successfully written
    bot.send_message(message.chat.id, "Squat workout saved successfully!")
