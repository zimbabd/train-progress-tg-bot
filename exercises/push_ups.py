import datetime


def handle_push_ups(bot, call, exercise_repo, training_repo):
    """
    Function for processing the 'push-up' exercise.
    """
    # Get the exercise ID
    template_id = int(call.data.split('_')[-1])

    # Get the template of the exercise by ID (in this case push-ups)
    template = exercise_repo.get_template_by_id(template_id)

    if template and template['template_name'] == 'push_ups':
       # If a pattern is found and it is “push-ups”, we begin asking for parameters
        bot.send_message(call.message.chat.id, "Enter the number of repetitions:")
        bot.register_next_step_handler(call.message,
                                       lambda m: process_reps(m, bot, exercise_repo, training_repo, template_id))
    else:
        bot.send_message(call.message.chat.id, "Error: Exercise not found.")


def process_reps(message, bot, exercise_repo, training_repo, template_id):
    # We get the number of repetitions
    try:
        reps = int(message.text)  # Convert to integer
        if reps <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Error: Please enter a positive number for the number of repetitions.")
        bot.register_next_step_handler(message,
                                       lambda m: process_reps(m, bot, exercise_repo, training_repo, template_id))
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
        bot.register_next_step_handler(message,
                                       lambda m: process_sets(m, bot, exercise_repo, training_repo, template_id, reps))
        return

    bot.send_message(message.chat.id, "Enter weight (in kg if available, otherwise leave blank):")

    # Register the next step to get the weight
    bot.register_next_step_handler(message,
                                   lambda m: process_weight(m, bot, exercise_repo, training_repo, template_id, reps,
                                                            sets))


def process_weight(message, bot, exercise_repo, training_repo, template_id, reps, sets):
   # Get the weight
    weight = message.text.strip() if message.text else None # If weight is not specified, save as None
    if weight and not weight.isdigit():
        bot.send_message(message.chat.id, "Error: Please enter a valid value for weight.")
        bot.register_next_step_handler(message,
                                       lambda m: process_weight(m, bot, exercise_repo, training_repo, template_id, reps,
                                                                sets))
        return

    weight = float(weight) if weight else None  # If weight is not specified, save as None
    user_id = message.from_user.id  # Get the user ID

    # Save the training session in the database
    training_repo.add_training_session(
        user_id=user_id,
        template_id=template_id,
        quantity=reps,
        sets=sets,
        weight=weight,
        session_date=datetime.datetime.now()
    )

    # Notify the user that the data was successfully written
    bot.send_message(message.chat.id, "Push-up workout saved successfully!")
