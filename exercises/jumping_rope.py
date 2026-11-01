import datetime
from telebot import types

def handle_jumping_rope(bot, call, exercise_repo, training_repo):
    """
   Function for processing the exercise "jumping with a rope".
    """
   # We get the exercise ID
    template_id = int(call.data.split('_')[-1])


   # We get the template of the match by ID
    template = exercise_repo.get_template_by_id(template_id)

    if template and template['template_name'] == 'jumping_rope':
        # If the pattern is found and it is "jumping with a rope", we start the parameter request
        bot.send_message(call.message.chat.id, "Enter the number of jumping rope:")
        bot.register_next_step_handler(call.message,
                                       lambda m: process_reps(m, bot, exercise_repo, training_repo, template_id))
    else:
        bot.send_message(call.message.chat.id, "Error: Exercise not found.")

def process_reps(message, bot, exercise_repo, training_repo, template_id):
    # Get the number of jumps

    try:
        reps = int(message.text)  # Convert to integer
        if reps <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for the number of jumps.")
        return

    bot.send_message(message.chat.id, "Enter the number of sets:")

    # Register the next step to get the number of sets
    bot.register_next_step_handler(message,
                                   lambda m: process_sets(m, bot, exercise_repo, training_repo, template_id, reps))

def process_sets(message, bot, exercise_repo, training_repo, template_id, reps):
    # Get the number of sets
    try:
        sets = int(message.text)  # Convert to integer
        if sets <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for the number of sets.")
        return

    bot.send_message(message.chat.id, "Enter the duration (in seconds) of one set:")

    # Register the next step to get the duration of one approach
    bot.register_next_step_handler(message,
                                   lambda m: process_duration(m, bot, exercise_repo, training_repo, template_id, reps, sets))

def process_duration(message, bot, exercise_repo, training_repo, template_id, reps, sets):
    # Get the duration of one approach (in seconds)
    try:
        duration = int(message.text)  # Convert to integer (seconds)
        if duration <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for duration.")
        return

    user_id = message.from_user.id  # Get the user ID

   # Save the training session in the database
    try:
        training_repo.add_training_session(
            user_id=user_id,
            template_id=template_id,
            quantity=reps,
            sets=sets,
            duration=duration,
            session_date=datetime.datetime.now(),

        )
        bot.send_message(message.chat.id, "Jumping rope workout saved successfully!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error when saving workout: {str(e)}")
