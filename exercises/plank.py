import datetime

def handle_plank(bot, call, exercise_repo, training_repo):
    """
    Function for processing the 'plank' exercise.
    """
    # Get the exercise ID
    template_id = int(call.data.split('_')[-1])

    # Get the exercise template by ID (in this case plank)
    template = exercise_repo.get_template_by_id(template_id)

    if template and template['template_name'] == 'plank':
        # If the template is found and it is a "bar", we begin to request parameters
        bot.send_message(call.message.chat.id, "Enter duration in seconds:")
        bot.register_next_step_handler(call.message,
                                       lambda m: process_duration(m, bot, exercise_repo, training_repo, template_id))
    else:
        bot.send_message(call.message.chat.id, "Error: Exercise not found.")

def process_duration(message, bot, exercise_repo, training_repo, template_id):
    # Get the duration of the plank
    try:
        duration = int(message.text)  # Convert to integer (seconds)
        if duration <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for duration.")
        return

    bot.send_message(message.chat.id, "Enter the number of sets:")

    # Register the next step to get the number of sets
    bot.register_next_step_handler(message,
                                   lambda m: process_sets(m, bot, exercise_repo, training_repo, template_id, duration))

def process_sets(message, bot, exercise_repo, training_repo, template_id, duration):
    # Get the number of sets
    try:
        sets = int(message.text)  # Convert to integer
        if sets <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for the number of sets.")
        return

    user_id = message.from_user.id  # Getting the user ID

    # Save the training session in the database
    try:
        training_repo.add_training_session(
            user_id=user_id,
            template_id=template_id,
            duration=duration,
            sets=sets,
            session_date=datetime.datetime.now()
        )
        bot.send_message(message.chat.id, "Plank workout saved successfully!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error when saving workout: {str(e)}")
